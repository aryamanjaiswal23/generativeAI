import openai
import os
import json
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import langchain

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
llm = ChatOpenAI(temperature=0, model_kwargs={"engine": "GPT3-5"})
tools = load_tools(["llm-math", "wikipedia"], llm=llm)


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
)

agent("What is 25 percent of 300")
prompt = """
J Robert Oppenheimer is a famous scientist.\ 
What did he do which made him famous?
"""
result = agent(prompt)

new_agent = create_python_agent(llm, tool=PythonREPLTool, verbose=True)
customer_list = [
    ["Harrison", "Chase"],
    ["Lang", "Chain"],
    ["Dolly", "Too"],
    ["Elle", "Elem"],
    ["Geoff", "Fusion"],
    ["Trance", "Former"],
    ["Jen", "Ayai"],
]
new_prompt = f"""Sort these customers by \ last name and then first name \ and print the output: {customer_list}"""
agent.run(new_prompt)

from langchain.agents import tool
from datetime import date


@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())


agents = initialize_agent(
    tools + [time],
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
)
# langchain.debug = True
try:
    result = agents("whats the date today?")
except:
    print("exception on external access")
# langchain.debug = False
