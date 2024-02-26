import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.memory import XataChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_tool
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.tools.search_internet import SearchInternet
from src.tools.search_lca_db import SearchLCADB
from src.tools.search_vector_db import SearchVectorDB
from src.tools.search_esg import SearchESG

load_dotenv()

def init_chat_history(session_id: str) -> BaseChatMessageHistory:
    xata_api_key = os.getenv("XATA_API_KEY")
    xata_db_url = os.getenv("XATA_DB_URL")
    xata_table_name = os.getenv("XATA_TABLE_NAME")

    return XataChatMessageHistory(
        session_id=session_id,
        api_key=xata_api_key,
        db_url=xata_db_url,
        table_name=xata_table_name,
    )

def openai_agent():
    # lc_tools = [SearchInternet(), SearchVectorDB(), SearchLCADB(), SearchESG()]
    lc_tools = [SearchESG()]
    oai_tools = [format_tool_to_openai_tool(tool) for tool in lc_tools]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are recognized as an authority on Environmental, Social, and Governance (ESG) issues. Your expertise encompasses comprehensive insights and detailed knowledge on sustainability, corporate social responsibility, ethical practices, and the environmental impacts of businesses. In your responses, commence with a succinct summary or overview of the topic. Subsequently, elaborate on the critical elements, offering an in-depth exploration or analysis of each key point."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4-turbo-preview",
    )

    agent = (
        {
            "input": lambda x: x["input"].encode("utf-8").decode("unicode_escape"),
            "history": lambda x: x["history"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm.bind(tools=oai_tools)
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(
        agent=agent, tools=lc_tools, verbose=True, handle_parsing_errors=True
    )

    agent_executor_with_history = RunnableWithMessageHistory(
        runnable=agent_executor,
        get_session_history=init_chat_history,
        history_messages_key="history",
    )

    return agent_executor_with_history
