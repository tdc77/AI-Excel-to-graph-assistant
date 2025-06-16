from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import (
    search_tool,
    save_tool,
    graph_from_excel_tool,
    get_excel_metadata_tool
)

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# LLM and parser setup
llm = ChatOpenAI(model="gpt-4o-mini")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     """You are a Data Analyst that helps generate graphs from Excel files.
     Use tools when needed. If you're unsure of sheet/column names, call 'get_excel_metadata'.
     If you’re asked to make a graph and don’t know the sheet or column names, use get_excel_metadata first.
     Wrap your final answer in this format:\n{format_instructions}"""),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

# Add tools
tools = [
    search_tool,
    save_tool,
    graph_from_excel_tool,
    get_excel_metadata_tool
]

agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run interaction
query = input("What can I help you create? ")
raw_response = agent_executor.invoke({"query": query})

# Parse and display result
try:
    structured_response = parser.parse(raw_response["output"])
    print("\nStructured Result:\n", structured_response)
except OutputParserException as e:
    print("Failed to parse output:\n", raw_response["output"])
except Exception as e:
    print("Unexpected error:", e)