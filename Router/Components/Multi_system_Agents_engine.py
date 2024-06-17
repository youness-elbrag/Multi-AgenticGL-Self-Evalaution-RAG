from engine.Complier import Complier
from utils.Helper import stream_data
from Model.Memory import History_Memory

def run_msa_planner_agent(query, model, temp,st):
    compiler = Complier(query=query, model=model, temp=temp, st_context=st)
    return compiler.EngineAgent()

def Agents_engine(prompt:str ,temp: float ,model_name:str ,st):
    if model_name in st.session_state.list_model:
        with st.spinner("Processing your request..."):
            generated_response = run_msa_planner_agent(prompt, model_name, temp,st)
            response = "\n".join(generated_response)
            if response is not None:
                with st.chat_message("assistant"):
                    st.write_stream(stream_data(response))
            History_Memory(prompt,response,st)
    else:
        st.error("Model is not available. Please Selected the downloaded Agent-LLM.")
        
        
