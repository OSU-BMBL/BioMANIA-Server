
import os
import pytest
import shutil
from unittest.mock import patch
import unittest
from pathlib import Path

from src.file_operations import (
    upload_session_file,
    remove_session_file,
    obtain_session_file,
    obtain_session_files,
)

class FileOperationsTestCase(unittest.TestCase):
    def setUp(self):
        shutil.copy("./tests/data/random-filename.csv", "/tmp/random-filename.csv")
        return super().setUp()
    
    def tearDown(self):
        # delete database file
        db_path = Path("./tests/data", "uploaded_files.db")
        db_path.unlink()

        # delete session directory
        session_path = Path("./tests/data", "123")
        files = session_path.glob("*.csv")
        for f in files:
            f.unlink()
        session_path.rmdir()

        return super().tearDown()

    @patch.dict(os.environ, {"DATA_FOLDER": "./tests/data"})    
    def test_upload_session_file(self):
        file_id = upload_session_file("123", "/tmp/random-filename.csv", "test.csv")
        meta_data = obtain_session_file(file_id)
        session_file = Path("./tests/data/123", meta_data["random_filename"])
        assert session_file.exists()

    @patch.dict(os.environ, {"DATA_FOLDER": "./tests/data"})    
    def test_remove_session_file(self):
        file_id = upload_session_file("123", "/tmp/random-filename.csv", "test.csv")
        meta_data = obtain_session_file(file_id)
        session_file = Path("./tests/data/123", meta_data["random_filename"])
        assert session_file.exists()

        res = remove_session_file(file_id)
        assert res
        assert session_file.exists() # we won't really delete the file, only mark it deleted in database
        meta_data = obtain_session_file(file_id)
        assert meta_data is None


