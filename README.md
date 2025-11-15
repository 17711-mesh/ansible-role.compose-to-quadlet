# README.md
# Ansible Role: compose-to-quadlet

This role wraps the Python project `python.compose-to-quadlet` to generate Podman Quadlet units from a Docker/Podman Compose file.

## Requirements

- Ansible
- Podman

## Role Variables

See `defaults/main.yml` for a list of variables and their default values.

## Example Playbook

```yaml
- name: Generate Quadlet units
  hosts: all
  become: true
  roles:
    - role: ansible-role.compose-to-quadlet
      vars:
        compose_to_quadlet_src_repo: "https://github.com/17711-mesh/python.compose-to-quadlet"
        compose_to_quadlet_src_path: "/opt/python.compose-to-quadlet"
        compose_file_path: "/opt/test-data/docker-compose.yml"
        quadlet_output_dir: "/etc/containers/systemd"
        quadlet_stack_name: "my-stack"
```

## Testing with Molecule

This role includes Molecule tests with the Podman driver to ensure its functionality.

### Setup

1.  **Create a Python Virtual Environment:**
    ```bash
    python3 -m venv .venv
    ```
2.  **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    Install Molecule, Molecule Podman plugin, and Ansible Core:
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file should contain:
    ```
    molecule
    molecule-plugins[podman]
    ansible-core==2.16.0
    ```

### Running Tests

To run the Molecule tests, navigate to the role's root directory and execute:

```bash
molecule test
```

This command will:
1.  Destroy any existing Molecule instances.
2.  Create a new Podman container instance (`ubuntu:latest`).
3.  Prepare the instance by installing Python and copying a sample `docker-compose.yml`.
4.  Converge the instance by applying the `ansible-role.compose-to-quadlet` role.
5.  Verify idempotence (run converge again and check for no changes).
6.  Run Testinfra tests to verify the generated Quadlet files.
7.  Destroy the instance.

### Debugging Tests

To debug a specific stage, you can run individual Molecule commands:

-   `molecule create`: Create the test instance.
-   `molecule converge`: Apply the role to the instance.
-   `molecule verify`: Run verification tests.
-   `molecule destroy`: Destroy the test instance.

You can also SSH into the running instance after `molecule create` or `molecule converge` using `molecule login`.