
import os
from datetime import datetime
from pathlib import Path as PathlibPath
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
import logging
from werkzeug.utils import secure_filename

from src.constants import DATA_FOLDER, ERROR_INVALID_INPUT, ERROR_OK, ERROR_UNKNOWN
from src.utils import allowed_file

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["File", "Files"]
)

@router.get("/v1/file/{session_id}/{filename}", description="download file")
def download_file(session_id: str, filename: str):
    try:
        if ".." in filename or filename.startswith(("/", "\\")):
            raise HTTPException(
                status_code=400,
                detail="Invalid filename. Directory traversal is not allowed."
            )

        data_folder = PathlibPath(os.environ.get(DATA_FOLDER, "./data"))
        file_path = data_folder / session_id / filename
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

@router.post("/v1/file/{session_id}", description="upload file")
def upload_file(session_id: str, file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file sent")
    if file.filename == '':
        return {"error": "No selected file", "code": ERROR_INVALID_INPUT}
    if not allowed_file(file.filename):
        return {"error": "File type not allowed", "code": ERROR_INVALID_INPUT}
    
    try:
        filename = secure_filename(file.filename)
        data_folder = os.environ.get(DATA_FOLDER, "./data")
        session_folder = os.path.join(data_folder, str(session_id))
        if not os.path.exists(session_folder):
            os.makedirs(session_folder)
        file_path = os.path.join(session_folder, filename)
        with open(file_path, "wb+") as fobj:
            fobj.write(file.file.read())
        
        return {"code": ERROR_OK, "filename": filename, "message": "File uploaded successfully"}
    except Exception as e:
        logger.error(str(e))
        return {"code": ERROR_INVALID_INPUT}

@router.delete("/v1/file/{session_id}/{filename}", description="delete file")
def delete_file(session_id: str, filename: str):
    data_folder = PathlibPath(os.environ.get(DATA_FOLDER, "./data"))
    session_folder = data_folder / session_id
    file_path = session_folder / filename
    try:
        if not file_path.exists():
            return {"code": ERROR_INVALID_INPUT, "error": f"Failed to delete file {filename}, no such file existed"}
        os.unlink(file_path)
        return {"code": ERROR_OK}
    except Exception as e:
        logger.error(e)
        return {"code": ERROR_UNKNOWN, "error": str(e)}

@router.get("/v1/files/{session_id}/list", description="list all files")
def list_files(session_id: str):
    data_folder = PathlibPath(os.environ.get(DATA_FOLDER))
    session_folder = data_folder / session_id
    if not session_folder.exists():
        return {"code": ERROR_OK, "files": []}
    try: 
        for r, d, files in os.walk(session_folder):
            break
        session_files = [{
            "filename": f,
            "filesize": os.path.getsize(session_folder / f),
            "created_at": datetime.fromtimestamp(os.path.getctime(session_folder / f)),
            "modified_at": datetime.fromtimestamp(os.path.getmtime(session_folder / f))
        } for f in files]
        return {"code": ERROR_OK, "files": session_files}
    except Exception as e:
        logger.error(str(e))
        return {"code": ERROR_UNKNOWN, "error": str(e)}



