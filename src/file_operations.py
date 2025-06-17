
import os
from pathlib import Path
import logging
import shutil
import uuid

from .database.file_database import (
    select_uploaded_file,
    select_session_uploaded_files,
    insert_uploaded_file,
    remove_uploaded_file,
)

logger = logging.getLogger(__name__)

def obtain_session_file(id: int):
    return select_uploaded_file(id)

def upload_session_file(
    session_id: str,
    tmpfile: str,
    filename: str,
):
    data_dir = Path(os.environ.get("DATA_FOLDER"))
    if not data_dir.exists():
        return None
    session_dir = data_dir / session_id
    try:
        if not session_dir.exists():
            session_dir.mkdir(exist_ok=True)
        random_fn = uuid.uuid4().hex[:12] + "-"+filename
        dst_fn = session_dir / random_fn
        shutil.move(tmpfile, dst_fn)
    except Exception as e:
        logger.error(e)
        return None
    id = insert_uploaded_file(
        session_id,
        filename,
        random_fn,
    )

    return id
    
def obtain_session_files(
    session_id: str
):
    return select_session_uploaded_files(session_id=session_id)

def remove_session_file(
    id: int,
):
    return remove_uploaded_file(id)
    
        


