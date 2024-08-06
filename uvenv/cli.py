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

import sys
import logging
from docopt import docopt

from .uv import UV
from .project import Project
from .__version__ import __version__

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    args = docopt(__doc__, version=f"uvenv {__version__}")
    uv = UV()
    project = Project.from_cwd()

    try:
        # Display information about the project.
        if args["info"]:
            print(f"uvenv {__version__}")
            uv.version()
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
                uv.run("pip", "install", *packages)

                # Add the packages to the requirements.in file.
                with open(project.path_to_requirements_in, "a") as f:
                    for package in packages:
                        f.write(f"{package}\n")

                # Update the lockfile.
                uv.run(
                    "pip",
                    "compile",
                    str(project.path_to_requirements_in),
                    "-o",
                    str(project.path_to_requirements_txt),
                )

            else:
                # Install the packages from the lockfile.
                uv.run("pip", "install", "-r", str(project.path_to_requirements_txt))

        # Uninstall packages.
        elif args["uninstall"]:
            packages = args["<packages>"]

            # Uninstall the packages.
            uv.run("pip", "uninstall", *packages)

            # Remove the packages from the requirements.in file.
            with open(project.path_to_requirements_in, "r") as f:
                lines = f.readlines()
            with open(project.path_to_requirements_in, "w") as f:
                for line in lines:
                    if line.strip() not in packages:
                        f.write(line)

            # Update the lockfile.
            uv.run(
                "pip",
                "compile",
                str(project.path_to_requirements_in),
                "-o",
                str(project.path_to_requirements_txt),
            )

        # Update the lockfile.
        elif args["lock"]:
            # Update the lockfile.
            uv.run(
                "pip",
                "compile",
                "-o",
                str(project.path_to_requirements_txt),
                str(project.path_to_requirements_in),
            )

        elif args["run"]:
            print("Run command not implemented.")
            sys.exit(1)

        elif args["shell"]:
            # This is a placeholder. You might want to use a library like `pty` to spawn an interactive shell
            print("Shell command not implemented.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
