from langchain.prompts import PromptTemplate


PROMPT_GRADER = PromptTemplate(
    template="""
System: You are tasked with determining if a project description is relevant to a user-described project based on keywords in the provided CSV file. \n
Your goal is to filter out irrelevant results without being overly strict.\n
Provide a binary score ('yes' or 'no') formatted as a JSON object with a single key 'score'. \n
If the answer is 'no', include the message: "I don't know the answer; it is out of my knowledge or is irrelevant to what I built for."'n

Format:
"score": "yes" or "no",
"message": "I don't know the answer; it is out of my knowledge or is irrelevant to what I built for." (only if 'no')

If Score is Yes Don't Include "message" JSON object . \n


User:
Here is the retrieved project information:
{document}

Here is the user-described project:
{project}
""",
    input_variables=["project", "document"],
)