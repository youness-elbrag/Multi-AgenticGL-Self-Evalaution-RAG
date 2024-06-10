import os
import subprocess
from langchain_community.chat_models import ChatOllama

class LLM:
    def __init__(self, type_return=None, temp=None, model_name="llama3", name_agent=None):

        self.local_llm = ["llama3"]
        self.default_model = model_name
        os.environ['LOCAL_LLM'] = ','.join(self.local_llm)
        self.type_return = type_return
        self.temp = temp
        self.agent_type = name_agent

    def agent(self):
        """
        Initialize the ChatOllama model based on the return type and temperature.
        """

        if self.default_model not in self.local_llm:
            model = self.list_model(self.default_model)
        else:
            model = self.default_model
        
        if self.type_return == "JSON":
            return ChatOllama(model=model, format="json", temperature=self.temp)
        else:
            #ChatOpenAI(api_key="ollama",model=self.default_model,base_url="http://localhost:11434/v1",temperature= 0)
            return ChatOllama(model=model, temperature=self.temp)

    def list_model(self, model_name):
        """
        Check if the model is in the local LLM list.
        If not, initiate a download for the model.

        Args:
            model_name (str): The name of the model to check.

        Returns:
            str: The model name if it is available locally.

        Raises:
            ValueError: If the model is not available locally and needs to be downloaded.
        """
        if model_name in self.local_llm:
            return model_name
        else:
            command = f"ollama pull {model_name} &"
            
            # Use subprocess.Popen to start the process in the background
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Downloading model {model_name}. Process ID:", process.pid)
            self.local_llm.append(model_name)
            return model_name

if __name__ == "__main__":
    llm_instance = LLM(type_return=None, temp=0.0, name_agent="example_agent")
    model_instance = llm_instance.agent()
    # print(model_instance)
    # print(llm_instance.list_model("new_model"))
    
    respond = model_instance.invoke("say hi")
    print(respond)
