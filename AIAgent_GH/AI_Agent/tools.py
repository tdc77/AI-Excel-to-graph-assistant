from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool, StructuredTool
from datetime import datetime
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os


documents_dir = os.path.expanduser("~/Documents")
# -----------------------------
# Tool 1: Save to Text File
# -----------------------------

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"


save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file."
)


# -----------------------------
# Tool 2: Get Excel Metadata
# -----------------------------

class ExcelMetadataInput(BaseModel):
    file_path: str

def get_excel_metadata(file_path: str) -> dict:
    try:
        xl = pd.ExcelFile(file_path)
        metadata = {}
        for sheet in xl.sheet_names:
            df = xl.parse(sheet, nrows=1)
            metadata[sheet] = list(df.columns)
        return metadata
    except Exception as e:
        raise ValueError(f"Failed to read Excel metadata: {str(e)}")

get_excel_metadata_tool = StructuredTool.from_function(
    func=get_excel_metadata,
    name="get_excel_metadata",
    description="Use this tool to see all sheet names and column names in an Excel file before plotting.",
    args_schema=ExcelMetadataInput
)


# -----------------------------
# Tool 3: Graph from Excel
# -----------------------------

class ExcelGraphInput(BaseModel):
    file_path: str
    sheet_name: str
    x_column: str
    y_column: str
    chart_type: str = "line"

def graph_from_excel(file_path: str, sheet_name: str, x_column: str, y_column: str, chart_type: str = "line") -> str:
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        return f"Error reading Excel file: {str(e)}"

    if x_column not in df.columns or y_column not in df.columns:
        return f"Invalid column names. Available columns: {', '.join(df.columns)}"

    plt.figure(figsize=(10, 6))
    if chart_type == "line":
        plt.plot(df[x_column], df[y_column])
    elif chart_type == "bar":
        plt.bar(df[x_column], df[y_column])
    elif chart_type == "scatter":
        plt.scatter(df[x_column], df[y_column])
    else:
        return f"Unsupported chart type: {chart_type}"

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{chart_type.title()} chart of {y_column} vs {x_column}")
    plt.grid(True)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png", dir=documents_dir)
    plt.savefig(temp_file.name)
    plt.close()

    return f"Chart saved to: {temp_file.name}"

graph_from_excel_tool = StructuredTool.from_function(
    func=graph_from_excel,
    name="graph_from_excel",
    description="Generate a graph from an Excel file. Requires sheet name, x and y column names.",
    args_schema=ExcelGraphInput
)


# -----------------------------
# Tool 4: Web Search 
# -----------------------------

search_tool = Tool(
    name="search",
    func=DuckDuckGoSearchRun().run,
    description="Search the web for information."
)

