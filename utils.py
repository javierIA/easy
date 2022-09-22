from importlib.resources import path
import os


def remove_whitespace_from_path(name):
    os.rename(name, name.replace(" ", ""))
    return name.replace(" ", "")
