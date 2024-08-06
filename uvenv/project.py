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
    def path_to_requirements(self):
        """The path to the project's `requirements.txt` file."""
        return self.path / "requirements.txt"

    @property
    def path_to_lockfile(self):
        """The path to the project's `requirements.lock` file."""
        return self.path / "requirements.lock"

    @property
    def path_to_venv(self):
        """The path to the project's virtual environment."""
        return self.path / ".venv"
