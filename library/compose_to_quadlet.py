#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import os
import yaml
from pathlib import Path
import tempfile
import shutil
import filecmp

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        project_path=dict(type='path', required=True),
        compose_file=dict(type='path', required=True),
        output_dir=dict(type='path', required=True),
        stack_name=dict(type='str', required=False, default=None),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    project_path = Path(module.params['project_path'])
    compose_file = Path(module.params['compose_file'])
    output_dir = Path(module.params['output_dir'])
    stack_name = module.params['stack_name']

    # Add project_path to sys.path to allow importing the library
    # This needs to be done before importing compose_to_quadlet
    if str(project_path) not in sys.path:
        sys.path.insert(0, str(project_path))

    try:
        # The library expects to be imported as 'compose_to_quadlet'
        # So we need to ensure the parent directory of 'compose_to_quadlet' is in sys.path
        # If project_path is /opt/python.compose-to-quadlet, then /opt/python.compose-to-quadlet
        # should be in sys.path
        from compose_to_quadlet.schemas import ComposeFile
        from compose_to_quadlet.generator import QuadletGenerator
    except ImportError as e:
        module.fail_json(msg=f"Failed to import compose_to_quadlet library. Ensure it's installed and project_path is correct. Error: {e}. sys.path: {sys.path}")

    changed = False
    result_files = []

    # Ensure output_dir exists
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        changed = True # Directory creation counts as a change

    # Create a temporary directory for generation
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmp_output_dir = Path(tmpdir_str)

        # Load compose file
        try:
            raw_compose_content = compose_file.read_text()
            raw_compose = yaml.safe_load(raw_compose_content)
            compose = ComposeFile.from_raw(raw_compose)
        except Exception as e:
            module.fail_json(msg=f"Failed to parse compose file {compose_file}: {e}")

        # Determine template directory
        template_dir = project_path / "compose_to_quadlet" / "templates"
        if not template_dir.is_dir():
            module.fail_json(msg=f"Template directory not found: {template_dir}")

        # Generate Quadlet units into the temporary directory
        try:
            gen = QuadletGenerator(template_dir)
            gen.generate(compose, tmp_output_dir, stack_name)
        except Exception as e:
            module.fail_json(msg=f"Failed to generate quadlet units: {e}")

        # Compare generated files with existing files in output_dir
        # and copy if different or new
        for generated_file in tmp_output_dir.iterdir():
            target_file = output_dir / generated_file.name
            result_files.append(str(target_file))

            if not target_file.exists() or not filecmp.cmp(generated_file, target_file, shallow=False):
                changed = True
                if not module.check_mode:
                    shutil.copy2(generated_file, target_file)
                    module.log(f"Copied/updated {target_file}")
            else:
                module.log(f"File {target_file} is identical, no change needed.")

        # Clean up any files in output_dir that were not generated
        # This ensures idempotence for removed services/networks/volumes
        existing_files_in_output = {f.name for f in output_dir.iterdir() if f.is_file()}
        generated_file_names = {f.name for f in tmp_output_dir.iterdir()}

        for extra_file_name in existing_files_in_output - generated_file_names:
            extra_file_path = output_dir / extra_file_name
            if extra_file_path.is_file(): # Ensure it's a file, not a subdirectory
                changed = True
                if not module.check_mode:
                    os.remove(extra_file_path)
                    module.log(f"Removed extra file {extra_file_path}")

    module.exit_json(changed=changed, msg="Quadlet units generated successfully.", files=result_files)

if __name__ == '__main__':
    run_module()