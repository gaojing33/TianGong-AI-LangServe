import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.tools import BaseTool

load_dotenv()

llm_model = os.getenv("OPENAI_MODEL")
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)


class AutoESGCheck(BaseTool):
    name = "ESG Compliance Summarizer"
    description = "Analyzes and summarizes Environmental, Social, and Governance (ESG) compliance information from provided texts, presenting the findings in Markdown format."

    def _run(self, upstream_outputs: str) -> str:
        """Use the tool synchronously."""
        response = client.chat.completions.create(
            model=llm_model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in Environmental, Social, and Governance (ESG) matters.""",
                },
                {
                    "role": "user",
                    "content": """Based on upstream outputs, provide a summary focusing on data disclosure, and write a summary for each segment identified by its task ID. Follow the Markdown structure below, modifying the title to match the task ID:

                    ### Task_ID_Example
                    - **Concluding Statement**: Provide a clear, initial verdict on the disclosure status.
                    - **Detailed Analysis**: Offer a comprehensive examination of the specifics, maintaining a narrative style.

                    ### Scope_1_emissions_data
                    - Begin with a conclusive statement regarding information disclosure.
                    - Elaborate with specific details in continuous prose.

                    ### Scope_1_emissions_breakdown
                    - Begin with a conclusive statement regarding information disclosure.
                    - Elaborate with specific details in continuous prose.

                    ... (Continue with additional task IDs, summarizing each in the same structured manner.)

                    Upstream outputs:
                    """
                    + upstream_outputs,
                },
            ],
        )
        output = response.choices[0].message.content
        return output


    async def _arun(self, upstream_outputs: str) -> str:
        """Use the tool asynchronously."""
        response = client.chat.completions.create(
            model=llm_model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in Environmental, Social, and Governance (ESG) matters.""",
                },
                {
                    "role": "user",
                    "content": """Based on upstream outputs, provide a summary focusing on data disclosure, and write a summary for each segment identified by its task ID. Follow the Markdown structure below, modifying the title to match the task ID:

                    ### Task_ID_Example
                    - **Concluding Statement**: Provide a clear, initial verdict on the disclosure status.
                    - **Detailed Analysis**: Offer a comprehensive examination of the specifics, maintaining a narrative style.

                    ### Scope_1_emissions_data
                    - Begin with a conclusive statement regarding information disclosure.
                    - Elaborate with specific details in continuous prose.

                    ### Scope_1_emissions_breakdown
                    - Begin with a conclusive statement regarding information disclosure.
                    - Elaborate with specific details in continuous prose.

                    ... (Continue with additional task IDs, summarizing each in the same structured manner.)

                    Upstream outputs:
                    """
                    + upstream_outputs,
                },
            ],
        )
        output = response.choices[0].message.content
        return output
