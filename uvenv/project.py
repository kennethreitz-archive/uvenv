from pathlib import Path

# PATHS = {
#     "requirements": "requirements.txt",
#     "lockfile": "requirements.lock",
#     "venv": ".venv",
# }

class Project:
    def __init__(self, path):
        self.path = Path(path).resolve()

    @classmethod
    def from_cwd(cls, *, search_depth=3, search_fname="requirements.txt"):
        """Find the project root by searching up the directory tree for a file named `requirements.txt`."""
        current_path = Path.cwd()
        for _ in range(search_depth):
            if (current_path / search_fname).exists():
                return cls(current_path)
            current_path = current_path.parent
        raise Exception(f"No {search_fname} found")

    @property
    def path_to_requirements_in(self):
        """The path to the project's `requirements.in` file."""
        path = self.path / "requirements.in"
        if path.exists():
            return path

    @property
    def path_to_requirements_txt(self):
        """The path to the project's `requirements.txt` file."""
        path = self.path / "requirements.txt"
        if path.exists():
            return path

    @property
    def path_to_venv(self):
        """The path to the project's virtual environment."""
        path = self.path / ".venv"
        if path.exists():
            return path
