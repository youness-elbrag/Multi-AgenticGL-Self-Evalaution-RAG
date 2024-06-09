from re import template
from .Agents.Agents import (
     Grader_Agent,
     planner_agent,
     feedback_agent,
     expert_agent
     )
from .VectorDB.Chorma import Retriever
from .Prompts.PromptExpert import PROMPT_EXPERT
from .Prompts.PromptFeedback import PROMPT_FEEDBACK
from .Prompts.PromptPLanner import PROMPT_PLANNER
from .Prompts.PromptGrader import PROMPT_GRADER



### Nodes


def retrieve_node(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    project = state["project"]
    model = state["model"]
    temp = state["temp"]
    print(model, temp , project)

    

    # Retrieval
    retriever = Retriever()
    documents = retriever.invoke(project)
    return {"documents": documents , "project": project,"model":model, "temp":temp}


def planner(state):
    """
    Generate answer using RAG on retrieved documents.

    Args:
        state (dict): The current graph state.

    Returns:
        dict: Updated state with LLM generation.
    """
    print("---PLANNER---")
    project = state["project"]
    documents = state["documents"]
    model = state["model"]
    temp = state["temp"]

    prediction = planner_agent(project, PROMPT_PLANNER, documents, model, temp)
    return {"documents": documents, "project": project, "prediction": prediction,"model":model, "temp":temp}

def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state.

    Returns:
        dict: Updated state with filtered documents and grading result.
    """
    print("---CHECK DOCUMENT RELEVANCE TO PROJECT---")
    project = state["project"]
    documents = state["documents"]
    model = state["model"]
    temp = state["temp"]

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    score = Grader_Agent(project, PROMPT_GRADER, documents, model, temp)
    grade = score["score"]
    filtered_docs = []

    if grade.lower() == "yes":
        print("---GRADE: DOCUMENT RELEVANT---")
        filtered_docs.append(format_docs(documents))
    else:
        print("---GRADE: DOCUMENT NOT RELEVANT---")
        grade = score['message']

    return {"documents": filtered_docs, "project": project, "Grade": grade, "prediction": grade,"model":model, "temp":temp}

def decide_to_generate(state):
    """
    Determines whether to generate an answer or add web search.

    Args:
        state (dict): The current graph state.

    Returns:
        str: Decision for next node to call.
    """
    print("---ASSESS GRADED DOCUMENTS---")
    grade = state["Grade"]

    if grade != "yes":
        print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO PROJECT---")
        return "not support"
    else:
        print("---DECISION: PREDICTION---")
        return "Planner"

def grade_generation_v_documents_and_project(state):
    """
    Determines whether the generation is grounded in the document and answers the project.

    Args:
        state (dict): The current graph state.

    Returns:
        str: Decision for next node to call.
    """
    print("---CHECK FEEDBACK---")
    project = state["project"]
    documents = state["documents"]
    prediction = state["prediction"]
    model = state["model"]
    temp = state["temp"]

    score = feedback_agent(documents, PROMPT_FEEDBACK, prediction, model, temp)
    grade = score["score"]

    if grade == "yes":
        print("---DECISION: PREDICTION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION VS PROJECT---")
        score = expert_agent(project, PROMPT_EXPERT, prediction, model, temp)
        grade = score["score"]

        if grade == "yes":
            print("---DECISION: PREDICTION ADDRESSES PROJECT---")
            return "useful"
        else:
            print("---DECISION: PREDICTION DOES NOT ADDRESS PROJECT---")
            return "Expert"
    else:
        print("---DECISION: PREDICTION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "Feedback"
