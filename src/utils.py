
import base64
import os
from typing import List, Optional, Tuple
import uuid
import nbformat
from nbconvert import HTMLExporter
from traitlets.config import Config

from src.constants import TOKEN_DAILY_LIMITATION
from src.datatypes import AuthTypeEnum
from src.llm_auth import llm_get_auth_type, llm_get_user_name_and_model
from src.token_usage_database import get_token_usage
from src.database.task_database import upsert_scanpy_task, select_scanpy_task

def get_rag_agent_prompts() -> List[str]:
    return [
        "The user has provided additional background information from scientific "
        "articles.",
        "Take the following statements into account and specifically comment on "
        "consistencies and inconsistencies with all other information available to "
        "you: {statements}",
    ]
    
def need_restrict_usage(client_key: str, model: str) -> Tuple[bool, int]:
    auth_type = llm_get_auth_type(client_key=client_key)
    if auth_type == AuthTypeEnum.ClientOpenAI or \
       auth_type == AuthTypeEnum.ClientWASM:
        return False, -1
    limitation = int(os.environ.get(TOKEN_DAILY_LIMITATION, -1))
    if limitation < 0:
        return False, -1
    user_name, actual_model = llm_get_user_name_and_model(
        client_key=client_key,
        session_id=None,
        model=model,
    )
    token_usage = get_token_usage(user_name, actual_model)
    return token_usage["total_tokens"] >= limitation, limitation

def allowed_file(filename: str):
    # TODO: need to implement later
    return True

def assign_cell_ids(nb_node):
    # Assign unique IDs to cells that lack them
    for cell in nb_node.cells:
        if 'metadata' not in cell:
            cell['metadata'] = {'id': uuid.uuid4().hex[:12]}
        elif 'id' not in cell['metadata']:
            cell['metadata']['id'] = uuid.uuid4().hex[:12]

    return nb_node

def convert_ipynb_to_html(json_str: str):
    """
    Convert a Jupyter notebook to HTML format using nbconvert.
    This function converts notebook json string to HTML.
    """
    nb_node = nbformat.reads(json_str, as_version=4)
    nb_node = assign_cell_ids(nb_node)
    c = Config()
    # c.HTMLExporter.exclude_input_prompt = True  # Equivalent to --no-prompt
    c.HTMLExporter.template_name = "cellid-template"        # Use 'lab' template; replace with your custom template name if needed
    html_exporter = HTMLExporter(config=c)
    (body, resources) = html_exporter.from_notebook_node(nb_node)

    return body

def post_process_context(session_id: str, contexts: list[tuple[str, str]]) -> list[tuple[str, str]]:
    ## fixme: currently, post_processor only handles the case of Scanpy APIAgent 
    ipynb = ""
    with open("tests/data/demo.ipynb", "r", encoding="utf-8") as f:
        ipynb = f.read()
    task_id = uuid.uuid4().hex
    upsert_scanpy_task(session_id, task_id, ipynb)
    
    return [{
        "mode": "api_scanpy",
        "context": [(task_id, "task_id")]
    }]




