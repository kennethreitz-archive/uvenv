# uvenv

**Note:** This project is a work in progress. Some features may not be fully implemented or may change in the future.


uvenv is a Python project management tool that leverages the speed of [uv](https://github.com/astral-sh/uv) for dependency management and virtual environment creation. It provides a simple interface for managing Python projects, inspired by tools like pipenv, but using requirements.txt and requirements.in files.

## Philosophy

- **Simplicity**: uvenv aims to provide a simple and intuitive interface for managing Python projects.
- **Speed**: uvenv leverages the speed of uv for dependency management and virtual environment creation.
- **Flexibility**: uvenv aims to be flexible and support a variety of project structures and workflows.
- **Compatibility**: uvenv aims to be compatible with a variety of Python versions and platforms.
- **Minimalism**: uvenv aims to be minimal and avoid unnecessary complexity.
- **Power**: uvenv aims to provide powerful features for managing Python projects.
- **Community**: uvenv aims to be community-driven and open-source.

## Features

- Automatic project root discovery
- Virtual environment management
- Dependency installation and uninstallation
- Requirements locking
- Command running within the virtual environment
- Interactive shell with activated virtual environment

## Installation

To install uvenv, you need to have Python 3.6+ and uv installed. Then you can install uvenv using pip:

```
pip install uvenv
```

## Usage

uvenv provides the following commands:

### Install

Install dependencies or specific packages:

```
uvenv install
uvenv install <package1> <package2>
```

### Uninstall

Remove specific packages:

```
uvenv uninstall <package1> <package2>
```

### Lock

Generate or update requirements.txt:

```
uvenv lock
```

### Run

Run a command within the virtual environment:

```
uvenv run <command>
```

### Shell

Spawn a new shell with the virtual environment activated:

```
uvenv shell
```

### Help

Show help message:

```
uvenv --help
```

## Project Structure

uvenv expects your project to have either a `requirements.txt` or `requirements.in` file in the project root. It will automatically discover the project root by searching for these files in the current directory and its parents.

## Examples

1. Start a new project:
   ```
   mkdir myproject
   cd myproject
   echo "requests==2.26.0" > requirements.in
   uvenv install
   ```

2. Add a new package:
   ```
   uvenv install numpy
   ```

3. Remove a package:
   ```
   uvenv uninstall requests
   ```

4. Update locked requirements:
   ```
   uvenv lock
   ```

5. Run a Python script:
   ```
   uvenv run python myscript.py
   ```

6. Start an interactive shell:
   ```
   uvenv shell
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
