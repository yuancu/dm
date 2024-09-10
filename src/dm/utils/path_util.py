"""
This module provides utility functions for working with file paths.
"""
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


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


class DirectoryManager:
    """
    A directory manager that simplifies directory creation and access.

    Attributes:
        dir_root (Path): The root directory path.
    """
    def __init__(self, root='.'):
        self.root = Path(root)

    def __getitem__(self, path):
        return DirectoryProxy(self.root, path)


class DirectoryProxy:
    """
    A class representing a directory proxy.

    Args:
        base_path (str): The base path of the directory.
        current_path (str): The current path of the directory.

    Attributes:
        base_path (str): The base path of the directory.
        current_path (str): The current path of the directory.
        full_path (str): The full path of the directory.
    """
    def __init__(self, base_path, current_path):
        self.base_path = base_path
        self.current_path = current_path
        self.full_path = self.base_path / self.current_path
        if not self.full_path.exists():
            self.full_path.mkdir(parents=True, exist_ok=True)
            logger.info("Created directory: %s", self.full_path)

    def __getitem__(self, path):
        return DirectoryProxy(self.full_path, path)

    def __str__(self):
        return str(self.full_path)

    def resolve(self):
        """Return the full path of the directory"""
        return self.full_path.resolve()
