from typing_extensions import TypedDict
from typing import List


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        project: project
        prediction: LLM Ttansfomer prediction
        documents: list of CSV file Data Project Description and Tasks
    """

    project: str
    prediction: str
    Grade: str
    documents: List[str]
    model: str
    temp: float
