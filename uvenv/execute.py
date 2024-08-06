# Get the command to run
def execute(project, command):
command = " ".join(args["<command>"])

    # Construct the path to the virtual environment's Python interpreter
    venv_python = os.path.join(project.path_to_venv, "bin", "python")

    # Construct the full command to run in the virtual environment
    full_command = f"{venv_python} -c 'import os, sys; os.execvp(sys.argv[1], sys.argv[1:])' {command}"

    # Run the command using os.system
    exit_code = os.system(full_command)

    # Exit with the same code as the command
    sys.exit(exit_code >> 8)
