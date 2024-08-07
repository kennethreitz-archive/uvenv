"""uvenv: A uv-based Python project management tool

Usage:
  uvenv info
  uvenv version
  uvenv install [<packages>...]
  uvenv uninstall <packages>...
  uvenv lock
  uvenv run [<command>...]
  uvenv shell
  uvenv (-h | --help)
  uvenv --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import os
import sys
import logging
import shlex
from docopt import docopt

from .project import Project
from .__version__ import __version__

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    args = docopt(__doc__, version=f"uvenv {__version__}")
    project = Project.from_cwd()

    # Ensure the project has a virtual environment.
    project.ensure()

    try:
        # Display information about the project.
        if args["info"]:
            print(f"uvenv {__version__}")
            # system_uv.version()
            print(f"project {project.path}")
            print(f"requirements {project.path_to_requirements_in}")
            print(f"lockfile {project.path_to_requirements_txt}")

        # Report the version of uvenv.
        elif args["version"]:
            print(f"uvenv {__version__}")

        # Install packages.
        elif args["install"]:
            packages = args["<packages>"]

            # If a package was provided, install it, and update the lockfile.
            if packages:
                # Install the packages.
                project.install(*packages)

            else:
                # Install the packages from the lockfile.
                project.install_from_lockfile()

        # Uninstall packages.
        elif args["uninstall"]:
            packages = args["<packages>"]

            # Uninstall the packages.
            project.uninstall(*packages)

            # Update the lockfile.
            project.lock()

        # Update the lockfile.
        elif args["lock"]:
            # Update the lockfile.
            project.lock()

        elif args["run"]:
            # Get the command to run
            command = shlex.join(*args["<command>"])

            # Construct the path to the virtual environment's Python interpreter
            venv_python = os.path.join(project.path_to_venv, "bin", "python")

            # Construct the full command to run in the virtual environment
            full_command = f"{venv_python} -c 'import os, sys; os.execvp(sys.argv[1], sys.argv[1:])' {command}"

            # Run the command using os.system
            exit_code = os.system(full_command)

            # Exit with the same code as the command
            sys.exit(exit_code >> 8)

        elif args["shell"]:
            print("Shell command not implemented.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
