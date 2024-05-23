from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from utils import format_docs
from .Ollama import LLM
from langchain_core.templates import PromptTemplate 

 # Assuming this is where PromptTemplate is imported from

def Grader_Agent(query: str, prompt_template: PromptTemplate, vector_db, llm_model: str, temp: float) -> dict:
    """
    Grades the provided query using the specified LLM model and agent type.

    Args:
        query (str): The query to grade.
        prompt_template (PromptTemplate): The prompt template to use.
        vector_db: The vector database to retrieve context from.
        llm_model (str): The name of the LLM model to use.
        agent_type (str): The type of agent to use.
        temp (float): The temperature setting for the LLM model.

    Returns:
        dict: The graded response.
    """
    context = vector_db.invoke(query)
    documents = format_docs(context)
    llm_instance = LLM(type_return="JSON", temp=temp, model_name=llm_model, name_agent="Grader")
    llm = llm_instance.agent()
    retrieval_grader = prompt_template | llm | JsonOutputParser()
    graded_response = retrieval_grader.invoke({"project": prompt_template, "document": documents})
    return graded_response

# result = grader(query, prompt_template, vector_db, llm_model, agent_type, temp)
# print(result)



def planner_agent(query: str, prompt_template: PromptTemplate, retriever, llm_model: str, temp: float) -> dict:
    """
    Plans tasks based on the provided query using the specified LLM model.

    Args:
        query (str): The query to plan tasks for.
        prompt_template (PromptTemplate): The prompt template to use.
        retriever: The retriever to use for additional context.
        llm_model (str): The name of the LLM model to use.
        temp (float): The temperature setting for the LLM model.

    Returns:
        dict: The planned tasks and pipelines.
    """
    llm_instance = LLM(type_return=None, temp=temp, model_name=llm_model, name_agent="Planner")
    llm = llm_instance.agent()
    rag_chain = prompt_template | llm | StrOutputParser()
    tasks_pipelines = rag_chain.invoke({"project": query, "context": retriever})
    return tasks_pipelines

# tasks = planner_agent(query, prompt_template, retriever, llm_model, temp)
# print(tasks)



def feedback_agent(documents: str, prompt_template: PromptTemplate, tasks_pipeline, llm_model: str, temp: float) -> dict:
    """
    Provides feedback based on the given documents and tasks pipeline using the specified LLM model.

    Args:
        documents (str): The documents to be reviewed.
        prompt_template (PromptTemplate): The prompt template to use.
        tasks_pipeline: The tasks pipeline to be evaluated.
        llm_model (str): The name of the LLM model to use.
        temp (float): The temperature setting for the LLM model.

    Returns:
        dict: The feedback on the documents and tasks pipeline.
    """
    llm_instance = LLM(type_return="JSON", temp=temp, model_name=llm_model, name_agent="feedback")
    llm = llm_instance.agent()
    feedback_grader = prompt_template | llm | JsonOutputParser()
    feedback = feedback_grader.invoke({"documents": documents, "prediction": tasks_pipeline})
    return feedback

# feedback = feedback_agent(documents, prompt_template, tasks_pipeline, llm_model, temp)
# print(feedback)


def expert_agent(query: str, prompt_template: PromptTemplate, tasks_pipeline, llm_model: str, temp: float) -> dict:
    """
    Evaluates the given tasks pipeline using the specified LLM model and provides expert feedback.

    Args:
        query (str): The query to evaluate.
        prompt_template (PromptTemplate): The prompt template to use.
        tasks_pipeline: The tasks pipeline to be evaluated.
        llm_model (str): The name of the LLM model to use.
        temp (float): The temperature setting for the LLM model.

    Returns:
        dict: The evaluations and feedback on the tasks pipeline.
    """
    llm_instance = LLM(type_return="JSON", temp=temp, model_name=llm_model, name_agent="expert")
    llm = llm_instance.agent()
    expert_grader = prompt_template | llm | JsonOutputParser()
    evaluations = expert_grader.invoke({"project": query, "prediction": tasks_pipeline})
    return evaluations

# evaluations = expert_agent(query, prompt_template, tasks_pipeline, llm_model, temp)
# print(evaluations)

