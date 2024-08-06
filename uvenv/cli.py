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
from docopt import docopt

from .uv import UV
from .project import Project
from .__version__ import __version__


def main():
    args = docopt(__doc__, version=f'uvenv {__version__}')
    uv = UV()
    project = Project.from_cwd()

    if args['info']:
        print(f"uvenv {__version__}")
        print(f"python {sys.version}")
        uv.version()
        print('--')

        print(f"project: {project.path_to_requirements}")



    if args['version']:
        print(f"uvenv {__version__}")

    if args['install']:
        packages = args['<packages>']
        if packages:
            uv.pip_install(*packages)
        else:
            uv.pip_install()

    elif args['uninstall']:
        packages = args['<packages>']
        uv.pip('uninstall', *packages)

    elif args['lock']:
        uv.pip_compile()

    elif args['run']:
        command = args['<command>']
        uv.run(*command)

    elif args['shell']:
        uv.run('shell')

if __name__ == '__main__':
    main()
