from pathlib import Path

from ._constants import (
    REQUIREMENTS_IN,
    REQUIREMENTS_TXT,
    VENV_DIR,
)


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

    def _valid_path(self, path):
        """Returns a path, if it exists."""
        if path.exists():
            return path

    def ensure_venv(self, uv, *args):
        """Ensure the project has a virtual environment."""

        if not self.path_to_venv.exists():
            uv.run("venv", str(self.path_to_venv), *args)

    def lock(self, uv):
        """Lock the project's dependencies."""

        uv.run(
            "pip",
            "compile",
            str(self.path_to_requirements_in),
            "-o",
            str(self.path_to_requirements_txt),
        )

    def install(self, uv, *packages):
        """Install the project's dependencies."""

        # Ensure the project has a virtual environment.
        self.ensure_venv(uv=uv)

        # Install the packages.
        uv.run("pip", "install", *packages)

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
        self.lock(uv=uv)

    def install_from_lockfile(self, uv):
        """Install the project's dependencies from the lockfile."""

        # Ensure the project has a virtual environment.
        self.ensure_venv(uv=uv)

        # Install the packages from the lockfile.
        uv.run("pip", "install", "-r", str(self.path_to_requirements_txt))

    def uninstall(self, uv, *packages):
        """Uninstall the project's dependencies."""

        # Uninstall the packages.
        uv.run("pip", "uninstall", *packages)

        # Remove the packages from the requirements.in file.
        with open(self.path_to_requirements_in, "r") as f:
            lines = f.readlines()
        with open(self.path_to_requirements_in, "w") as f:
            for line in lines:
                if line.strip() not in packages:
                    f.write(line)

        self.lock(uv=uv)

    @property
    def path_to_requirements_in(self):
        """The path to the project's `requirements.in` file."""
        return self._valid_path(self.path / REQUIREMENTS_IN)

    @property
    def path_to_requirements_txt(self):
        """The path to the project's `requirements.txt` file."""
        return self._valid_path(self.path / REQUIREMENTS_TXT)

    @property
    def path_to_venv(self):
        """The path to the project's virtual environment."""
        return self._valid_path(self.path / VENV_DIR)
