import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.database.file_database import (
    insert_uploaded_file, 
    select_uploaded_file,
)

@patch.dict(os.environ, {"DATA_FOLDER": "./tests/data"})
def test_uploadedfile_database():
    id = insert_uploaded_file("123", "foo.txt", "123.txt")
    ret = select_uploaded_file(id)
    assert ret is not None
    assert ret["session_id"] == "123"

    db_path = Path("./tests/data", "uploaded_files.db")
    db_path.unlink()