import os

REQUIREMENTS_IN = os.environ.get("UVENV_REQUIREMENTS_IN", "requirements.in")
REQUIREMENTS_TXT = os.environ.get("UVENV_REQUIREMENTS_TXT", "requirements.txt")
VENV_DIR = os.environ.get("UVENV_VENV_DIR", ".venv")
UV_PATH = os.environ.get("UVENV_UV", "uv")
PYTHON = os.environ.get("UVENV_PYTHON", "python")
