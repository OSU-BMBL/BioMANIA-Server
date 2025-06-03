
from src.utils import convert_ipynb_to_html
from bs4 import BeautifulSoup, Tag
import re

def test_convert_ipynb_to_html():
    with open("tests/data/demo.ipynb", "r", encoding="utf-8") as f:
        json_str = f.read()
    html_output = convert_ipynb_to_html(json_str)
    assert html_output is not None
    assert "<!DOCTYPE html>" in html_output

    soup = BeautifulSoup(html_output, "html.parser")
    cells = soup.select("div.code_cell")
    pattern = re.compile(r"^cell-[a-fA-F0-9]{12}$")
    for cell in cells:
        try:
            id: str = cell.attrs.get("id")  # Ensure each cell has an id attribute
            res = pattern.match(id)
            assert res is not None, f"Cell ID {id} does not match the expected pattern"
        except Exception as e:
            assert False, f"Error processing cell: {e}"
            


