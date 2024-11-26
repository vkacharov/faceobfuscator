import os
import sys

def load_file_path(file_name):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    env_path = os.path.join(base_path, file_name)
    return env_path
    