"""uvenv: A uv-based Python project management tool

Usage:
  uvenv info
  uvenv version
  uvenv install [<packages>...]
  uvenv uninstall <packages>...
  uvenv lock
  uvenv run [<command>]
  uvenv shell
  uvenv (-h | --help)
  uvenv --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import sys
from docopt import docopt

from .uv import UV
from .project import Project
from .__version__ import __version__


def main():
    args = docopt(__doc__, version=f"uvenv {__version__}")
    uv = UV()
    project = Project.from_cwd()

    lock_command = [
        "pip",
        "compile",
        "-o",
        project.path_to_requirements_txt,
        project.path_to_requirements_in,
    ]
    install_command = ["pip", "pip", "install", *(args["<packages>"] or [])]
    install_all_command = ["pip", "install", "-r", project.path_to_requirements_txt]
    uninstall_command = ["pip", "uninstall", *(args["<packages>"] or [])]
    uninstall_all_command = ["pip", "uninstall", "-r", project.path_to_requirements_txt]
    run_command = ["run", *(args["<command>"] or [])]

    if args["info"]:
        print(f"uvenv {__version__}")
        uv.version()
        print(f"project {project.path}")
        print(f"requirements {project.path_to_requirements_in}")
        print(f"lockfile {project.path_to_requirements_txt}")

    if args["version"]:
        print(f"uvenv {__version__}")

    if args["install"]:
        if args["<packages>"]:
            uv.run(*install_command)
        else:
            uv.run(*install_all_command)

        # TODO: insert package into requirements.in
        # with open(project.path_to_requirements_in, "a") as f:
        # f.write(f"{packages}\n")

        # TODO: lock.
        uv.run(*lock_command)

    elif args["uninstall"]:
        packages = args["<packages>"]

        if packages:
            uv.run(*uninstall_command)
        else:
            uv.run(*uninstall_all_command)

    elif args["lock"]:
        uv.run(*lock_command)

    elif args["run"]:
        command = args["<command>"]
        uv.run(*run_command)

    elif args["shell"]:
        print("Shell command not implemented.")
        exit(1)


if __name__ == "__main__":
    main()
