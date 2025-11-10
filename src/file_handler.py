"""
File handler client for managing data persistence.
"""

import os
from datetime import datetime
from typing import Optional


class FileHandler:
    """Handle file operations for data persistence. Singleton pattern."""

    _instance = None

    def __new__(cls, file_path: str = "dummy_db.txt"):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super(FileHandler, cls).__new__(cls)
            cls._instance.file_path = file_path
        return cls._instance

    def write_data(self, data: str, include_timestamp: bool = True) -> bool:
        """
        Append data to the file.

        Args:
            data: The string data to write to the file
            include_timestamp: Whether to prepend a timestamp (default: True)

        Returns:
            bool: True if write was successful, False otherwise
        """
        try:
            # Prepare the data to write
            if include_timestamp:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_data = f"[{timestamp}] {data}\n"
            else:
                formatted_data = f"{data}\n"

            # Append to file (create if doesn't exist)
            with open(self.file_path, 'a') as f:
                f.write(formatted_data)

            return True

        except Exception as e:
            print(f"Error writing to file: {e}")
            return False

    def read_all(self) -> Optional[str]:
        """
        Read all contents from the file.

        Returns:
            str: File contents or None if file doesn't exist
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    return f.read()
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def file_exists(self) -> bool:
        """
        Check if the file exists.

        Returns:
            bool: True if file exists, False otherwise
        """
        return os.path.exists(self.file_path)
