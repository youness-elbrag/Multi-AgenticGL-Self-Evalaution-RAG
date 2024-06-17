from langchain.prompts import PromptTemplate


PROMPT_EXPERT = PromptTemplate(
    template="""
System: You are an expert assessing whether an answer is useful in resolving a question. \n
Provide a binary 'yes' or 'no' score to indicate whether the answer is useful. \n
Format the score as a JSON object with a single key 'score' and no preamble or explanation.\n

User:
Here is the answer:
-------
{prediction}
-------
Here is the project:
{project}

Assistant:
""",
    input_variables=["prediction", "project"],
)