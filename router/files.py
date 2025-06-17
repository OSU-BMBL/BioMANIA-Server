
import os
from datetime import datetime
from pathlib import Path as PathlibPath
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
import logging
from werkzeug.utils import secure_filename

from src.constants import DATA_FOLDER, ERROR_INVALID_INPUT, ERROR_OK, ERROR_UNKNOWN
from src.datatypes import UploadFilePostModel
from src.utils import allowed_file

from src.file_operations import (
    upload_session_file, 
    remove_session_file,
    obtain_session_files,
    obtain_session_file,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["File", "Files"]
)

@router.get("/v1/file/{file_id}", description="download file")
def download_file(file_id: int):
    try:
        metadata = obtain_session_file(id)
        filename = metadata["filename"]
        session_id = metadata["session_id"]
        random_filename = metadata["random_filename"]
        data_dir = PathlibPath(os.environ.get("DATA_FOLDER", "./data"))
        session_dir = data_dir / session_id
        fn = session_dir / random_filename

        if ".." in fn or fn.startswith(("/", "\\")):
            raise HTTPException(
                status_code=400,
                detail="Invalid filename. Directory traversal is not allowed."
            )
        
        file_path = fn
        print(f"Attempting to serve file from: {file_path}") # For debugging

        # Check if the file exists and is actually a file (not a directory)
        if not file_path.exists():
            print(f"File not found at: {file_path}")
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found for session '{session_id}'.")
        if not file_path.is_file():
            print(f"Path is not a file: {file_path}")
            raise HTTPException(status_code=400, detail=f"'{filename}' is not a valid file.")

        return FileResponse(
            path=file_path,
            filename=filename, # This is what the user's browser will suggest as the download name
            media_type='application/octet-stream' # Generic binary stream
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}") # Log the error
        raise HTTPException(status_code=500, detail="An internal server error occurred while trying to download the file.")

@router.post(
    "/v1/file/{session_id}", description="upload session file"
)
def uploadSessionFile(session_id: str, uploadFile: UploadFilePostModel):
    tmpFile = uploadFile.tmpFile
    filename = uploadFile.filename

    try:
        id = upload_session_file(session_id, tmpFile, filename)
        return {
            "code": ERROR_OK,
            "file_id": id,
        }
    except Exception as e:
        return {
            "error": str(e), "code": ERROR_UNKNOWN,
        }

@router.get(
    "/v1/files/{session_id}", description="get all uploaded session files"
)
def getSessionFiles(session_id: str):
    try: 
        files = obtain_session_files(session_id)
        return {
            "code": ERROR_OK,
            "files": files,
        }
    except Exception as e:
        return {
            "code": ERROR_UNKNOWN, "error": str(e),
        }

@router.delete(
    "/v1/file/{file_id}", description="remove uploaded file"
)
def removeUploadedFile(file_id: int):
    try:
        res = remove_session_file(file_id)
        return {"code": ERROR_OK}
    except Exception as e:
        return {
            "code": ERROR_UNKNOWN, "error": str(e),
        }

