import os
import sys
from pathlib import Path
import shlex

from ._constants import REQUIREMENTS_IN, REQUIREMENTS_TXT, VENV_DIR, PYTHON


def system_run(*command):
    """Run a system command and return the exit code."""
    exit_code = os.system(shlex.join(*command))
    return exit_code >> 8


class Project:
    def __init__(self, path):
        self.path = Path(path).resolve()

    @classmethod
    def from_cwd(cls, *, search_depth=3, search_fname=REQUIREMENTS_TXT):
        """Find the project root by searching up the directory tree for a file named `requirements.txt`."""
        current_path = Path.cwd()
        for _ in range(search_depth):
            if (current_path / search_fname).exists():
                return cls(current_path)
            current_path = current_path.parent
        raise Exception(f"No {search_fname} found")

    def run(self, *command):
        """Run a command in the project."""

        python = self.path_to_venv / "bin" / "python"
        if not python.exists():
            python = PYTHON

        command = shlex.join(command)

        full_command = f"{python} -c 'import os, sys; os.execvp(sys.argv[1], sys.argv[1:])' {command}"
        exit_code = os.system(full_command)

        return exit_code >> 8

    def ensure(self):
        """Ensure the project has a uv."""

        self.ensure_venv()
        self.ensure_uv()

    def ensure_venv(self, *args):
        """Ensure the project has a virtual environment."""

        if not self.path_to_venv.exists():
            self.run("uv", "venv", str(self.path_to_venv), "-p", PYTHON)

    def ensure_uv(self):
        """Ensure the project has a uv."""

        if not self.path_to_uv.exists():
            self.run("uv", "pip", "install", "uv")

    def lock(self):
        """Lock the project's dependencies."""

        # Ensure the project has a virtual environment.
        self.ensure()

        # Lock the dependencies.
        self.run(
            "uv",
            "pip",
            "compile",
            str(self.path_to_requirements_in),
            "-o",
            str(self.path_to_requirements_txt),
        )

    def install(self, *packages):
        """Install the project's dependencies."""

        # Ensure the project has a virtual environment.
        self.ensure()

        # Install the packages.
        self.run("uv", "pip", "install", *packages)

        # Add the packages to the requirements.in file.
        # Only add the packages that are not already in the file.
        with open(self.path_to_requirements_in, "r") as f:
            lines = f.readlines()

        # Add the packages to the requirements.in file.
        with open(self.path_to_requirements_in, "a") as f:
            for package in packages:
                if package.strip() not in lines:
                    f.write(f"{package}\n")

        # Update the lockfile.
        self.lock()

    def install_from_lockfile(self):
        """Install the project's dependencies from the lockfile."""

        # Ensure the project has a virtual environment.
        self.ensure()

        # Install the packages from the lockfile.
        self.run("uv", "pip", "install", "-r", str(self.path_to_requirements_txt))

    def uninstall(self, uv, *packages):
        """Uninstall the project's dependencies."""

        # Ensure the project has a virtual environment.
        self.ensure()

        # Uninstall the packages.
        self.run("uv", "pip", "uninstall", *packages)

        # Remove the packages from the requirements.in file.
        with open(self.path_to_requirements_in, "r") as f:
            lines = f.readlines()
        with open(self.path_to_requirements_in, "w") as f:
            for line in lines:
                if line.strip() not in packages:
                    f.write(line)

        self.lock()

    @property
    def path_to_requirements_in(self):
        """The path to the project's `requirements.in` file."""
        return self.path / REQUIREMENTS_IN

    @property
    def path_to_requirements_txt(self):
        """The path to the project's `requirements.txt` file."""
        return self.path / REQUIREMENTS_TXT

    @property
    def path_to_venv(self):
        """The path to the project's virtual environment."""
        return self.path / VENV_DIR

    @property
    def path_to_uv(self):
        """The path to the project's uv."""
        return self.path_to_venv / "bin" / "uv"
