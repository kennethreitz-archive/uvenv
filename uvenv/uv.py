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

    def help(self, *args):
        """Show help for a uv command."""
        return self.run("help", *args)

    def version(self, *args):
        """Show the uv version."""
        return self.run("version", *args)

    def venv(self, *args):
        """Create a new virtual environment."""
        return self.run("venv", *args)

    def pip(self, *args):
        """Run a pip command."""
        return self.run("pip", *args)

    def pip_compile(self, *args):
        """Generate a requirements.txt file."""
        return self.pip("compile", *args)

    def pip_sync(self, *args):
        """Sync the requirements.txt file."""
        return self.pip("sync", *args)

    def pip_install(self, *args):
        """Install a package."""
        return self.pip("install", *args)


    # Add more methods for other uv commands as needed
