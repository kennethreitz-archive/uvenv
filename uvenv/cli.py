"""uvenv: A uv-based Python project management tool

Usage:
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

from docopt import docopt


def main():

    def install(packages):
        if not packages:
            print("Installing all dependencies from requirements.in or requirements.txt")
        else:
            print(f"Installing packages: {', '.join(packages)}")

    def uninstall(packages):
        print(f"Uninstalling packages: {', '.join(packages)}")

    def lock():
        print("Generating PEP 751 compatible lock file")

    def run(command):
        if not command:
            print("No command provided to run")
        else:
            print(f"Running command: {' '.join(command)}")

    def shell():
        print("Spawning a new shell with the virtual environment activated")

    def show_help():
        print(__doc__)

    def show_version():
        print("uvenv version 1.0.0")

    def main():
        args = docopt(__doc__, version="1.0.0")

        if args['install']:
            install(args['<packages>'])
        elif args['uninstall']:
            uninstall(args['<packages>'])
        elif args['lock']:
            lock()
        elif args['run']:
            run(args['<command>'])
        elif args['shell']:
            shell()
        elif args['--help']:
            show_help()
        elif args['--version']:
            show_version()


if __name__ == "__main__":
    main()
