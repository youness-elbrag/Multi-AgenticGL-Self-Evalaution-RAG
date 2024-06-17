from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
import streamlit as st 

if "list_model" not in st.session_state:
    st.session_state["list_model"] = ["llama3","llama2"]

if "multi_task_df" not in st.session_state:
    st.session_state.multi_task_df = []

if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm A ***Multi-Agents System Based on Graph-Engine Built to Planing JESA Project Given Description*** . How can I help you today?")
        ]

for message in st.session_state.chat_history:
  if isinstance(message, AIMessage):
    with st.chat_message("AI"):
      st.markdown(message.content)
  elif isinstance(message, HumanMessage):
    with st.chat_message("Human"):
      st.markdown(message.content)
 
    
st.session_state.chat_history.append(HumanMessage(content=user_input))
st.session_state.chat_history.append(AIMessage(content=output_message)) # Moved inside the if block
