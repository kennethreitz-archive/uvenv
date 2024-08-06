"""A subprocess wrapper for uv using delegator."""

import os

from ._constants import UV


class UV:
    """A wrapper for the uv command line tool."""

    def __init__(self, executable=UV):
        """Initialize the uv wrapper."""
        self.executable = executable

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
