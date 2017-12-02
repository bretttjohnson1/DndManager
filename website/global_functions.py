import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def global_path_to_local_path(path_str):
    return os.path.join(BASE_DIR, path_str)