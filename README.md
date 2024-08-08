# uvenv

`uvenv` is a workflow tool for `uv`, inspired by Pipenv, designed to manage Python project dependencies using `requirements.txt` and `requirements.in` files. It aims to simplify dependency management and environment setup.

**Note**: this software is in early development and may not be suitable for production use.

## Features

- **Dependency Management**: Install packages listed in `requirements.in` and generate a lockfile (`requirements.txt`) for consistent environments.
- **Flexibility**: Customize file and directory locations using environment variables.
- **Ease of Use**: Thin wrapper around `$ uv pip compile` and `$ uv pip install` commands.

## Installation

To install `uvenv`, ensure you have Python 3.6+ and `uv` installed. Then, install `uvenv` using pip:
```sh
pip install uvenv-cli
```

## Project Structure

`uvenv` assumes the following structure:
- `requirements.in`: Lists the packages to be installed.
- `requirements.txt`: Lockfile with exact versions of packages.
- `.venv`: Directory for the virtual environment.

`uvenv` automatically discovers the project root by searching for these files in the current directory and its parents.

## Commands

- `$ uvenv install`: Install packages from `requirements.in`.
- `$ uvenv uninstall`: Uninstall packages listed in `requirements.in`.
- `$ uvenv lock`: Generate or update the lockfile (`requirements.txt`).

## Usage

1. **Start a New Project**:
    ```sh
    mkdir myproject
    cd myproject
    echo "requests==2.26.0" > requirements.in
    uvenv install
    ```
2. **Add a New Package**:
    ```sh
    uvenv install numpy
    ```
3. **Remove a Package**:
    ```sh
    uvenv uninstall requests
    ```
4. **Update Locked Requirements**:
    ```sh
    uvenv lock
    ```

## Environment Variables

Customize locations with environment variables:
- `UVENV_REQUIREMENTS_IN`: Path to the requirements input file (default: `requirements.in`)
- `UVENV_REQUIREMENTS_TXT`: Path to the lockfile (default: `requirements.txt`)
- `UVENV_VENV_DIR`: Directory for the virtual environment (default: `.venv`)
- `UVENV_UV`: Path to the `uv` executable (default: `uv`)
- `UVENV_PYTHON`: Python interpreter to use (default: `python`)

Example:
```sh
export UVENV_REQUIREMENTS_IN=requirements-dev.in
export UVENV_REQUIREMENTS_TXT=requirements-dev.txt
export UVENV_VENV_DIR=~/.venvs/myproject
uvenv install
```

## Upcoming Features

- `uvenv run`: Run a Python script.
- `uvenv shell`: Start an interactive shell.

## Contributing

Contributions are welcome! Please submit a Pull Request.

## License

This project is licensed under the MIT License.
