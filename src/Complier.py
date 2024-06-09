from .AgentGL import workflow
from pprint import pprint

class Complier:
    """
    A class to handle the compilation and execution of the workflow.
    """

    # Compile the workflow once, so it is ready for use
    app = workflow.compile(debug=False)

    def __init__(self, query: str, model: str, temp: float, st_context):
        """
        Initializes the Complier with the specified workflow parameters.

        Args:
            query (str): The query to be processed.
            model (str): The model to be used for processing.
            temp (float): The temperature parameter for the model.
            st_context: The Streamlit context to use for logging.
        """
        self.query = query
        self.model = model
        self.temp = temp
        self.st = st_context

    def EngineAgent(self):
        """
        Executes the compiled workflow with the provided inputs and returns the predictions.
        """
        inputs = {
            "project": self.query,
            "model": self.model,
            "temp": self.temp
        }
        predictions = []
        for output in self.app.stream(inputs):
            for key, value in output.items():
                self.st.write(f"Finished running Agent: {key}:")
                self.st.write(value)
                if "prediction" in value:
                    predictions.append(value["prediction"])
        return predictions


        
