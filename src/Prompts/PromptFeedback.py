from langchaim.prompts import PromptTemplate


PROMPT_FEEDBACK = PromptTemplate(
    template="""
System: You are an evaluator assessing whether an answer is grounded in or supported by a set of facts.\n
Provide a binary 'yes' or 'no' score to indicate whether the answer is supported by the facts.\n
Format the score as a JSON object with a single key 'score' and no preamble or explanation.\n

User:
Here are the facts:
-------
{documents}
-------
Here is the answer:
{prediction}

Evaluator:
""",
    input_variables=["prediction", "documents"],
)
