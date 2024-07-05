from logging import disable
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import time
from utils.Helper import stream_data
from utils.Helper import execute_extracted_code ,execute_pip_code
from .ReACT import ReACT_DataFrame_Agent
from Model.Memory import History_Memory
from langchain.memory import ConversationBufferMemory
from Model.Memory import History_Chat

memory = ConversationBufferMemory(memory_key="chat_history")

PROMPT_Helper_1 = """
System: You are tasked with performing data analysis and visualization using a given DataFrame named `df`.\n
- Follow these instructions: \n

1. If creating plots, use the Plotly library and ensure the figure is warmed up with `st.plotly_chart()` for web UI display support. \n
2. Provide the necessary pip install command for any required packages to be executed in a bash terminal.\n
3. Write the code in Python. \n
"""

PROMPT_Helper_2 = """
Below is the answer to your question along with the installation process for any required libraries:
"""


HANDLING_PROMPT_1 = """
Here's how to do it:

```
highest_estimated_task = df.loc[df['Predicted_Duration_Hours'].idxmax()]
print(highest_estimated_task)
```
"""

PREFIX = """
            You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
            You should use the tools below to answer the question posed of you:
            
         """

memory = ConversationBufferMemory(memory_key="chat_history")

def AgentExecutor(Agent,df,prompt,Helper_prompt):
    agent_analysis = create_pandas_dataframe_agent(
                Agent,df,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                handle_parsing_errors=HANDLING_PROMPT_1,
                max_iterations=15,
                early_stopping_method  = "force",
                memory=memory,
                return_intermediate_seps= True,
                allow_dangerous_code=True,
                )   
                

    adaptive_prompt = prompt  + Helper_prompt

    Analysis = agent_analysis.invoke(adaptive_prompt
    )
    return Analysis['output'] + PROMPT_Helper_2


def PromptEngineering(model_name,temp,prompt,st):
    agent = ChatOpenAI(
                        api_key="ollama",
                        model=model_name,
                        base_url="http://localhost:11434/v1",
                        temperature= temp,
                    )
    df = st.session_state.multi_task_df[-1]
    TYPEAGENT = st.radio(label="Chose The Agent to Use ",options=["ReACT-Agent","ExeCuTor-Agent"],captions = ["***Chose Agent-Type to Use in data analysis***"]) 

    if TYPEAGENT == "ExeCuTor-Agent":
        if prompt_agent := st.chat_input(f"ask Agent-Analysis for given Prediction to analysis..."):
            with st.chat_message("user"):
                st.markdown(prompt_agent)
            if model_name:
                if model_name in st.session_state.list_model:
                    with st.spinner("Reasoning Agent Executor Steps..."):
                        Respond = AgentExecutor(agent,df,prompt_agent,Helper_prompt=prompt)
                        with st.chat_message("assistant"):
                            st.write_stream(stream_data(Respond))
                            time.sleep(5)
                            execute_pip_code(Respond,st)   
                            execute_extracted_code(Respond,st)
                        History_Memory(prompt_agent,Respond,st)

            else:
                st.error("Model is not available. Please wait for the download to complete.")

    
    
            
       
    elif TYPEAGENT == "ReACT-Agent":
        if prompt_agent := st.chat_input(f"ask Agent-Analysis for given Prediction to analysis..."):
            with st.chat_message("user"):
                st.markdown(prompt_agent)
            if model_name:
                if model_name in st.session_state.list_model:
                    with st.spinner("Reasoning Agent Executor Steps..."):
                        AnalysisAgent = ReACT_DataFrame_Agent(agent,df,
                                max_iterations=15,
                                early_stopping_method  = "force",
                                return_intermediate_steps=True, 
                                verbose=True,
                                memory=memory,
                        )
                        Respond = AnalysisAgent.invoke(prompt_agent)
                        if Respond is not None:
                            with st.chat_message("assistant"):
                                st.write_stream(stream_data(Respond))
                            History_Memory(prompt_agent,Respond,st)

            else:
                st.error("Model is not available. Please wait for the download to complete.")

    else:
        st.error("Limited Selected Agent")



def AgentInterpter(toggle_statu_agent,st):

    if st.toggle("Agnet Analysis Result", value=toggle_statu_agent, disabled=False):
        if not st.session_state.multi_task_df:
            st.error("No data available. Please ensure there a Prediction Tasks in Session")
        else:
            st.markdown("#### Agent Interpter Statu: Activated ")
            History_Chat(st)

            col1 , _ = st.columns(2)
            with col1: 
                st.markdown("##### Settings Params")
                model_name = st.text_input("Model", placeholder="Enter model name here...")
                temp = st.slider("Temperature", min_value=0.0, max_value=0.7, value=0.0, step=0.1)

            PROMPT = st.radio(label="Chose's One of Helper Prompt",options=["Prompt-Helper" , "Costum-Prompt"],captions ="***Adding Costum Instruction***", horizontal=True) 
            if PROMPT == "Costum-Prompt" :
                with col1:
                    costum_prompt = st.text_input("Prompt", placeholder="write Costume Prompt here...")

                PromptEngineering(model_name,temp,costum_prompt,st)
            else:
                PROMPT = PROMPT_Helper_1
                PromptEngineering(model_name,temp,PROMPT,st)


            
            
            
