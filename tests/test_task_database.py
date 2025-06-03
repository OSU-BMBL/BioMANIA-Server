
import pytest
from src.task_database import upsert_scanpy_task, select_scanpy_task
import uuid

def test_task_database():
    task_id = uuid.uuid4().hex

    res = upsert_scanpy_task("1", task_id, "{\"cells\": []}")
    assert res is True, "Failed to upsert scanpy task"

    res = select_scanpy_task(task_id)
    assert res is not None, "Failed to select scanpy task"
    assert res["task_id"] == task_id, "Task ID does not match"
    assert res["session_id"] == "1", "Session ID does not match"
    assert res["ipynb"] == "{\"cells\": []}", "IPYNB content does not match"

