from pathlib import Path
import shutil
from typing import Union
import logging


class IoOperationError(Exception):
    """Custom exception for IO operations"""
    pass


class IoUtility:
    """Utility class for handling file system operations."""

    @staticmethod
    def write_temp_file(content: str, file_path: Union[str, Path]) -> None:
        try:
            file_path = Path(file_path)
            IoUtility.create_dir_if_not_exists(file_path.parent)
            file_path.write_text(content)
        except Exception as e:
            logging.error(f"Failed to write temp file {file_path}: {str(e)}")
            raise IoOperationError("Failed to write temp file.")

    @staticmethod
    def create_dir_if_not_exists(dir_path: Union[str, Path]) -> None:
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create directory {dir_path}: {str(e)}")
            raise IoOperationError("Failed to create directory.")

    @staticmethod
    def delete_dir_if_exists(dir_path: Union[str, Path]) -> None:
        try:
            path = Path(dir_path)
            if path.exists():
                shutil.rmtree(path)
        except Exception as e:
            logging.error(f"Failed to delete directory {dir_path}: {str(e)}")
            raise IoOperationError("Failed to delete directory.")
