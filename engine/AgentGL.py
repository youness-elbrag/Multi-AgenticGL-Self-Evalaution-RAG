from langgraph.graph import END, StateGraph
from .GraphState import GraphState
from .Nodes_agents import (
    retrieve_node,
    grade_documents,
    planner,
    decide_to_generate,
    grade_generation_v_documents_and_project,
)

# Initialize the workflow with the initial state
workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("retrieve", retrieve_node)  # Node to retrieve documents
workflow.add_node("grade_documents", grade_documents)  # Node to grade documents
workflow.add_node("Planner", planner)  # Node to plan based on documents

# Set the entry point of the workflow
workflow.set_entry_point("retrieve")

# Define the edges between the nodes
workflow.add_edge("retrieve", "grade_documents")  # Edge from retrieve to grade_documents

# Add conditional edges based on the decision to generate or not
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "not support": END,  # End the workflow if documents are not supported
        "Planner": "Planner",  # Proceed to Planner node if documents are relevant
    },
)

# Add conditional edges for the Planner node based on the grading of the generation
workflow.add_conditional_edges(
    "Planner",
    grade_generation_v_documents_and_project,
    {
        "Expert": "Planner",  # Loop back to Planner for further refinement
        "useful": END,  # End the workflow if the generation is useful
        "Feedback": "Planner",  # Loop back to Planner for feedback-based improvement
    },
)

   


