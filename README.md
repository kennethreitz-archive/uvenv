# `uvenv` — workflow tool for uv

This repository contains the command `uvenv`, a workflow tool for
[`uv`](https://pypi.org/project/uv/). The goal of `uvenv` is to provide much of
the functionality of tools like `pipenv`, but using `requirements.txt` and
`requirements.in` files, along with a `$ uv pip compile` step.

This may or may not be a good idea. We'll see.

## Status

- The `requirements.in` file is a "source of truth" for the project's dependencies.
  - I am considering adding support for other intake formats, such as `pyproject.toml` and `Pipfile`.
- The "point of interface" for `uvenv` is the resulting `requirements.txt` file.
  - Other tools can use this file to install the project's dependencies, however desired.
  - This should allow developers the ability to use it without forcing other members of their team to use `uvenv`. That is, they should be able to use `pip` or `uv` or whatever they want.
- The `uvenv` command is a thin wrapper around `$ uv pip compile` and `$ uv pip install`.
- The `uvenv` command is not yet feature-complete.
  - It currently only supports `install`, `uninstall`, and `lock` commands.
  - It does not yet support `run` or `shell` commands.

## Commands

`uvenv` currently provides the following primary commands:

- `$ uvenv install` — Install the packages in `requirements.in`.
- `$ uvenv uninstall` — Uninstall the packages in `requirements.in`.
- `$ uvenv lock` — Generate or update the lockfile in `requirements.txt`.


## Project Structure

`uvenv` assumes the following project structure:

- `requirements.in` — A file containing the packages to be installed.
- `requirements.txt` — A lockfile containing the exact versions of the packages to be installed.
- `.venv` — A directory containing the virtual environment.

`uvenv` will automatically discover the project root by searching for these files in the current directory and its parents.

## Environment Variables

`uvenv` allows you to customize the locations of key files and directories using environment variables:

- `UVENV_REQUIREMENTS_IN`: Specifies the location of the requirements input file (default: `requirements.in`)
- `UVENV_REQUIREMENTS_TXT`: Specifies the location of the requirements lockfile (default: `requirements.txt`)
- `UVENV_VENV_DIR`: Specifies the directory for the virtual environment (default: `.venv`)
- `UVENV_UV`: Specifies the path to the `uv` executable (default: `uv`)
- `UVENV_PYTHON`: Specifies the Python interpreter to use (default: `python`)

For example, to use a different name for your requirements file:

```shell
$ export UVENV_REQUIREMENTS_IN=requirements-dev.in
$ export UVENV_REQUIREMENTS_TXT=requirements-dev.txt
$ export UVENV_VENV_DIR=~/.venvs/myproject

$ uvenv install
```


## Installation

To install `uvenv`, you need to have Python 3.6+ and uv installed. Then you can install uvenv using pip:

```shell
$ pip install uvenv-cli
```

## Project Structure

uvenv expects your project to have either a `requirements.txt` or `requirements.in` file in the project root. It will automatically discover the project root by searching for these files in the current directory and its parents.

## Usage

1. Start a new project:
   ```shell
   $ mkdir myproject
   $ cd myproject
   $ echo "requests==2.26.0" > requirements.in
   $ uvenv install
   ```

2. Add a new package:
   ```shell
   $ uvenv install numpy
   ```

3. Remove a package:
   ```shell
   $ uvenv uninstall requests
   ```

4. Update locked requirements:
   ```shell
   $ uvenv lock
   ```

## Upcoming features

5. Run a Python script:
   ```shell
   $ uvenv run python myscript.py
   ```

6. Start an interactive shell:
   ```shell
   $ uvenv shell
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project will be licensed under the MIT License.
