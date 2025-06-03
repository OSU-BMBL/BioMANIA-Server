import os
from datetime import datetime
from pathlib import Path as PathlibPath
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
import logging
from werkzeug.utils import secure_filename

from src.constants import DATA_FOLDER, ERROR_INVALID_INPUT, ERROR_OK, ERROR_TASK_DATA_NOT_FOUND, ERROR_TASK_NOT_FOUND, ERROR_UNKNOWN
from src.utils import allowed_file, convert_ipynb_to_html
from src.task_database import select_scanpy_task

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["task", "tasks"]
)

@router.get("/v1/task/data/{session_id}/{task_id}", description="task data")
def get_task_data(session_id: str, task_id: str):
    data = select_scanpy_task(task_id)
    if data is None:
        return {"code": ERROR_TASK_NOT_FOUND, "error": "Task not found"}
    if "ipynb" not in data:
        return {"code": ERROR_TASK_DATA_NOT_FOUND, "error": "Task data not found"}
    ipynb = data["ipynb"]
    html = convert_ipynb_to_html(ipynb)

    return {
        "code": ERROR_OK,
        "ipynb": ipynb,
        "html": html,
    }
