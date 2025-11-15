import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_repo_cloned(host):
    f = host.file("/opt/python.compose-to-quadlet/pyproject.toml")
    assert f.exists
    assert f.is_file

def test_quadlet_output_dir_exists(host):
    d = host.file("/etc/containers/systemd")
    assert d.exists
    assert d.is_directory

def test_quadlet_files_generated(host):
    # Check for web.container and db.container
    web_container = host.file("/etc/containers/systemd/web.container")
    assert web_container.exists
    assert web_container.is_file
    assert "Image=nginx:alpine" in web_container.content_string

    db_container = host.file("/etc/containers/systemd/db.container")
    assert db_container.exists
    assert db_container.is_file
    assert "Image=postgres:13" in db_container.content_string

    # Check for molecule-stack.target
    stack_target = host.file("/etc/containers/systemd/molecule-stack.target")
    assert stack_target.exists
    assert stack_target.is_file
    assert "Wants=podman-web.service podman-db.service" in stack_target.content_string

    # Check for network and volume files if they were generated (our compose doesn't define them explicitly, but the library might create defaults)
    # For now, just check for the containers and target.

