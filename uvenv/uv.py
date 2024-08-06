"""A subprocess wrapper for uv using delegator."""

import os

from ._constants import UV_PATH


class UV:
    """A wrapper for the uv command line tool."""

    def __init__(self, executable=UV_PATH):
        """Initialize the uv wrapper."""
        self.executable = executable

    @classmethod
    def from_project(cls, project):
        """Create a uv wrapper from a project."""
        return cls(project.path_to_uv)

    def run(self, *args):
        """Run a uv command."""

        cmd = f"{self.executable} {' '.join([str(a) for a in args])}"
        os.system(cmd)

    def version(self):
        """Get the uv version."""
        return self.run("--version")

    # def run_announced(self, *args):
    #     print(f"Running: {self.executable} {' '.join([str(a) for a in args])}")
    #     self.run(*args)

    # Add more methods for other uv commands as needed
