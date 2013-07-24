import os

def make_dir(path):
    """Create path if it does not exist already"""
    if not os.path.exists(path):
        os.makedirs(path)
