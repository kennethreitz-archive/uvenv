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

import subprocess
import os
import sys
import platform

from docopt import docopt


__version__ = "0.1.0"

class Project:
    def __init__(self):
        self.home = self._find_project_home()
        self.venv_path = os.path.join(self.home, ".venv")
        self.requirements_in = os.path.join(self.home, "requirements.in")
        self.requirements_txt = os.path.join(self.home, "requirements.txt")

    def _find_project_home(self):
        current_dir = os.getcwd()
        while True:
            if os.path.exists(os.path.join(current_dir, "requirements.txt")) or \
               os.path.exists(os.path.join(current_dir, "requirements.in")):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                raise FileNotFoundError("Could not find project root with requirements.txt or requirements.in")
            current_dir = parent_dir

    def run_command(self, command):
        try:
            return subprocess.run(command, shell=True, check=True, text=True, capture_output=True, cwd=self.home)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Command output: {e.output}")
            sys.exit(1)

    def create_venv(self):
        if not os.path.exists(self.venv_path):
            print(f"Creating virtual environment in {self.venv_path}")
            self.run_command(f"uv venv {self.venv_path}")
        else:
            print(f"Virtual environment already exists in {self.venv_path}")

    def compile_requirements(self):
        if os.path.exists(self.requirements_in):
            print("Compiling requirements.in to requirements.txt")
            self.run_command(f"uv pip compile {self.requirements_in} -o {self.requirements_txt}")
        else:
            print("requirements.in not found. Skipping compilation step.")

    def install_dependencies(self, packages=None):
        if packages:
            package_list = " ".join(packages)
            print(f"Installing packages: {package_list}")
            self.run_command(f"uv pip install {package_list}")
            self.run_command(f"uv pip freeze > {self.requirements_txt}")
        elif os.path.exists(self.requirements_txt):
            print("Installing dependencies from requirements.txt")
            self.run_command(f"uv pip install -r {self.requirements_txt}")
        else:
            print("requirements.txt not found. Please create it or run 'uvenv lock' first.")

    def uninstall_dependencies(self, packages):
        package_list = " ".join(packages)
        print(f"Uninstalling packages: {package_list}")
        self.run_command(f"uv pip uninstall {package_list} -y")
        self.run_command(f"uv pip freeze > {self.requirements_txt}")

    def lock(self):
        if os.path.exists(self.requirements_in):
            print("Locking dependencies")
            self.compile_requirements()
        else:
            print("requirements.in not found. Creating from installed packages.")
            self.run_command(f"uv pip freeze > {self.requirements_txt}")

    def spawn_shell(self):
        if not os.path.exists(self.venv_path):
            print("Virtual environment not found. Creating one...")
            self.create_venv()

        # Determine the appropriate activation script based on the OS
        if platform.system() == "Windows":
            activate_script = os.path.join(self.venv_path, "Scripts", "activate.bat")
            shell = os.environ.get("COMSPEC", "cmd.exe")
        else:
            activate_script = os.path.join(self.venv_path, "bin", "activate")
            shell = os.environ.get("SHELL", "/bin/bash")

        # Prepare the command to run
        if platform.system() == "Windows":
            command = f'{shell} /K "{activate_script} && cd /d {self.home}"'
        else:
            command = f'{shell} -c "source {activate_script} && cd {self.home} && exec {shell}"'

        print(f"Spawning a new shell with the virtual environment activated...")
        subprocess.run(command, shell=True)

def main():
    arguments = docopt(__doc__, version=f"uvenv {__version__}")
    try:
        project = Project()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if arguments['install']:
        project.create_venv()
        if arguments['<packages>']:
            project.install_dependencies(arguments['<packages>'])
        else:
            project.compile_requirements()
            project.install_dependencies()
    elif arguments['uninstall']:
        project.uninstall_dependencies(arguments['<packages>'])
    elif arguments['lock']:
        project.lock()
    elif arguments['run']:
        if not arguments['<command>']:
            print("Error: No command specified to run")
            return
        cmd = " ".join(arguments['<command>'])
        project.run_command(f"{project.venv_path}/bin/python -m {cmd}")
    elif arguments['shell']:
        project.spawn_shell()

if __name__ == "__main__":
    main()
