"""uvenv: A uv-based Python project management tool

Usage:
  uvenv install
  uvenv lock
  uvenv (-h | --help)
  uvenv --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import sys
import logging

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

    try:
        # Ensure the project has a virtual environment.
        project.ensure_requirements_txt()
        project.ensure_venv()

        # Install packages.
        if args["install"]:
            project.install_from_lockfile()

        # Update the lockfile.
        elif args["lock"]:
            # Update the lockfile.
            project.lock()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
