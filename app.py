__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from streamlit_option_menu import option_menu
from src.Complier import Complier
import time

st.set_page_config(
    page_title="MSA-Multi-Agent-System Planner",
    layout="wide",
    initial_sidebar_state="auto",
)

def run_msa_planner_agent(query, model, temp):
    compiler = Complier(query=query, model=model, temp=temp, st_context=st)
    return compiler.EngineAgent()

list_model = ["llama3"]

with st.sidebar:
    st.markdown("## Settings")
    
    model_name = st.text_input("Model", placeholder="Enter model name here...")

    if model_name:
        if model_name not in list_model:
            with st.spinner(f"Downloading model {model_name}... ⏳"):
                time.sleep(4 * 60)  
                st.session_state.model_ready = True  
                list_model.append(model_name)
                st.success(f"Model {model_name} downloaded successfully.")
        else:
            st.success(f"Model {model_name} is already available.")

    temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    selected = option_menu(
        menu_title="Main Menu",
        options=["Info", "MSA Planner", "LTSM-Task-DP"],
        icons=["info-circle", "robot", "bar-chart-line-fill"],
        menu_icon="cast",
        default_index=1,
    )

# Info Section
if selected == "Info":
    st.markdown(
        "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
    )
    st.markdown("# Project Info")
    st.write("This project leverages a Multi-Agent System (MSA) Planner to manage tasks and strategies.")


# MSA Planner Section
if selected == "MSA Planner":
    st.markdown("# MSA Planner - Multi-Agent System")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Enter your query for the MSA Planner..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        if model_name:
            if model_name in list_model:
                with st.spinner("Processing your request..."):
                    generated_response = run_msa_planner_agent(prompt, model_name, temp)
                    response = "\n".join(generated_response)
                    
                    # Display assistant message in chat message container
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("Model is not available. Please wait for the download to complete.")

# Placeholder for future LSTM-related features
if selected == "LTSM-Task-DP":
    st.subheader("Prediction Task Duration (LSTM) - Coming Soon")
