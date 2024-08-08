import os
import sys
from pathlib import Path
import shlex

from ._constants import REQUIREMENTS_IN, REQUIREMENTS_TXT, VENV_DIR


def system_run(*command):
    """Run a system command and return the exit code."""
    exit_code = os.system(shlex.join(command))
    return exit_code >> 8

class Project:
    def __init__(self, path):
        self.path = Path(path).resolve()

    @classmethod
    def from_cwd(cls, *, search_depth=3, search_fnames=[REQUIREMENTS_TXT, REQUIREMENTS_IN]):
        """Find the project root by searching up the directory tree for a file named `requirements.txt`."""
        current_path = Path.cwd()

        for search_fname in search_fnames:
            for _ in range(search_depth):
                if (current_path / search_fname).exists():
                    return cls(current_path)
                current_path = current_path.parent

        raise Exception(f"No packaging files found!")

    def ensure_venv(self, *args):
        """Ensure the project has a virtual environment."""

        if not self.path_to_venv.exists():
           system_run("uv", "venv", str(self.path_to_venv))

    def ensure_requirements_txt(self):
        """Ensure the project has a `requirements.txt` file."""

        if not self.path_to_requirements_txt.exists():
            self.lock()

    def lock(self):
        """Lock the project's dependencies."""

        # Ensure the project has a virtual environment.
        self.ensure_venv()

        # Lock the dependencies.
        system_run(
            "uv",
            "pip",
            "compile",
            str(self.path_to_requirements_in),
            "-o",
            str(self.path_to_requirements_txt),
        )

    def install_from_lockfile(self):
        """Install the project's dependencies from the lockfile."""

        # Ensure the project has a virtual environment.
        self.ensure_venv()

        # Install the packages from the lockfile.
        system_run("uv", "pip", "install", "-r", str(self.path_to_requirements_txt))

    def uninstall(self, uv, *packages):
        """Uninstall the project's dependencies."""

        # Ensure the project has a virtual environment.
        self.ensure_venv()

        # Uninstall the packages.
        system_run("uv", "pip", "uninstall", *packages)

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

    @property
    def path_to_python(self):
        """The path to the project's Python executable."""
        return self.path_to_venv / "bin" / "python"
