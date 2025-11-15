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
    # Quadlet directory for rootless user
    d = host.file("/home/testops/.config/containers/systemd")
    assert d.exists
    assert d.is_directory
    assert d.user == "testops"
    assert d.group == "testops"

def test_quadlet_files_generated(host):
    # Check for web.container and db.container in user's quadlet directory
    web_container = host.file("/home/testops/.config/containers/systemd/web.container")
    assert web_container.exists
    assert web_container.is_file
    assert web_container.user == "testops"
    assert web_container.group == "testops"
    assert "Image=nginx:alpine" in web_container.content_string

    db_container = host.file("/home/testops/.config/containers/systemd/db.container")
    assert db_container.exists
    assert db_container.is_file
    assert db_container.user == "testops"
    assert db_container.group == "testops"
    assert "Image=postgres:13" in db_container.content_string

    # Check for molecule-stack.target in user's quadlet directory
    stack_target = host.file("/home/testops/.config/containers/systemd/molecule-stack.target")
    assert stack_target.exists
    assert stack_target.is_file
    assert stack_target.user == "testops"
    assert stack_target.group == "testops"
    assert "Wants=podman-web.service podman-db.service" in stack_target.content_string

def test_systemd_user_target_running(host):
    # Check if the systemd user service is running
    # This requires the systemd service to be started by the converge playbook
    target_service = host.service("podman-molecule-stack.target")
    assert target_service.is_running
    assert target_service.is_enabled

def test_path_configuration(host):
    # Verify PATH contains /opt/podman/bin and /opt/podman/libexec/podman
    path_env = host.run("sudo -iu testops printenv PATH").stdout
    assert "/opt/podman/bin" in path_env
    assert "/opt/podman/libexec/podman" in path_env

def test_ld_so_d_configuration(host):
    # Verify /opt/podman/lib is in ld.so.conf.d and ldconfig has been run
    ld_conf = host.file("/etc/ld.so.conf.d/podman.conf")
    assert ld_conf.exists
    assert ld_conf.is_file
    assert "/opt/podman/lib" in ld_conf.content_string
    # Check if ldconfig has picked it up (by trying to find a library from podman if possible, or just checking the file)
    # For simplicity, we'll just check the file presence and content for now.
    # A more robust check would involve `ldconfig -p | grep <some_podman_lib>`

