# Ansible Role: Compose to Quadlet.

> This role wraps the Python project `python.compose-to-quadlet` to generate Podman Quadlet units from a Docker/Podman Compose file.

## Table of Contents

* [Synopsis](#synopsis)
* [Requirements](#requirements)
* [Role Variables](#role-variables)
* [Example Playbook](#example-playbook)
* [Testing](#testing)
* [Changelog](#changelog)
* [License](#license)
* [Author Information](#author-information)


## Synopsis

This role wraps the Python project `python.compose-to-quadlet` to generate Podman Quadlet units from a Docker/Podman Compose file.

## Requirements

- Ansible
- Podman
- Optional: Molecule

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

## Testing

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

## Changelog

See [CHANGELOG](CHANGELOG.md) for a detailed history of changes.

## License

>
> [MIT License](LICENCE)
>
> Copyright (c) 2025, 🐌 [The 17711 Frame](https://17711.org)
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
> 

## Author Information

This project is maintained by 🐌 [The 17711 Frame](https://17711.org).

