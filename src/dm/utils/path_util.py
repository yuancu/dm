"""
This module provides utility functions for working with file paths.
"""
import os


def ensure_dir(path):
    """
    Ensure that a directory exists at the given path.
    
    Args:
        path (str): The path of the directory to be created.
    
    Returns:
        None
    """
    os.makedirs(path, exist_ok=True)


def ensure_parent_dir(path):
    """
    Ensure that the parent directory of the given path exists.
    
    Parameters:
        path (str): The path for which the parent directory needs to be ensured.
    """
    ensure_dir(os.path.dirname(path))
