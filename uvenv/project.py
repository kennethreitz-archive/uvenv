import os

class Project:
    def __init__(self, path):
        self.path = path


    def from_cwd(search_depth=3):
        for i in range(search_depth):
            if os.path.exists(os.path.join(os.getcwd(), "requirements.txt")):
                return Project(os.getcwd())
            os.chdir("..")
        raise Exception("No requirements.txt found")
