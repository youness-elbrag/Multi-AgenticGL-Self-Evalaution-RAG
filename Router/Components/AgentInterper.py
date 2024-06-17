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


PROMPT_Helper_1 =  """ 
   In DataFrame Given data to use  df 
 \n1. if Plots use plotly and  warm up The fig with st.plotly_chart() for support Web UI Display, 
 \n2. Set pip command Packages to instal In Bash at Once Terminal \n3. Code In Python langauge Progarmming 
 
 """
PROMPT_Helper_2 = """
\nhere the Following Answer given by your Question and Instalation Process Lib if was needed
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

memory = ConversationBufferMemory(memory_key="chat_history", input_key="input",return_messages=True)

def AgentExecutor(Agent,df,prompt,Helper_prompt,Memory=memory):
    agent_analysis = create_pandas_dataframe_agent(
                Agent,df,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                handle_parsing_errors=HANDLING_PROMPT_1,
                max_iterations=15,
                early_stopping_method  = "force",
                agent_executor_kwargs={"memory": Memory,  "return_intermediate_steps": True},
                memory=Memory,
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
                        Respond = AgentExecutor(agent,df,prompt_agent,Helper_prompt=prompt,Memory=memory)
                        with st.chat_message("assistant"):
                            st.write_stream(stream_data(Respond))
                            time.sleep(5)
                            execute_pip_code(Respond,st)   
                            execute_extracted_code(Respond,st)
                            History_Memory(prompt_agent,Respond,st)

            
       
    elif TYPEAGENT == "ReACT-Agent":
        prompt = PREFIX
        if prompt_agent := st.chat_input(f"ask Agent-Analysis for given Prediction to analysis..."):
            with st.chat_message("user"):
                st.markdown(prompt_agent)
            if model_name:
                if model_name in st.session_state.list_model:
                    with st.spinner("Reasoning Agent Executor Steps..."):
                        Respond = ReACT_DataFrame_Agent(agent,df,prefix=prompt,
                                max_iterations=15,
                                early_stopping_method  = "force",
                                return_intermediate_steps=True, 
                                memory=memory,
                        ).invoke(prompt_agent)
                        with st.chat_message("assistant"):
                            st.write_stream(stream_data(Respond))
                            time.sleep(5)
                            execute_pip_code(Respond,st)   
                            execute_extracted_code(Respond,st)
                            History_Memory(prompt_agent,Respond,st)

    else:
        st.error("Model is not available. Please wait for the download to complete.")


def AgentInterpter(toggle_statu_agent,st):

    if st.toggle("Agnet Analysis Result", value=toggle_statu_agent, disabled=False):
        if not st.session_state.multi_task_df:
            st.error("No data available. Please ensure there a Prediction Tasks in Session  to comp")
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
                st.write_stream(stream_data(PROMPT))
                PromptEngineering(model_name,temp,PROMPT,st)


            
            
            