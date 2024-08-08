"""uvenv: A uv-based Python project management tool

Usage:
  uvenv info
  uvenv version
  uvenv install
  uvenv lock
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

import shellingham
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
    project.ensure_venv()

    try:
        # Display information about the project.
        if args["info"]:
            print(f"uvenv {__version__}")
            # system_uv.version()
            print(f"python {project.path_to_python}")
            print(f"venv {project.path_to_venv}")
            print(f"project {project.path}")
            print(f"requirements {project.path_to_requirements_in}")
            print(f"lockfile {project.path_to_requirements_txt}")

        # Report the version of uvenv.
        elif args["version"]:
            print(f"uvenv {__version__}")

        # Install packages.
        elif args["install"]:
            project.install_from_lockfile()

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

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
