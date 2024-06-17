import streamlit as st
from streamlit_option_menu import option_menu
from utils.Helper import stream_data
from langchain_core.messages import AIMessage
from Router.Components.remove_model import remove_model
from Router.Components.add_model import Add_model
from Router.Components.Multi_system_Agents_engine import Agents_engine
from Router.Components.Estimation_planing import Estimation_tasks_and_projects
from Router.Components.dash import Analysis_dash
from Router.Components.AgentInterper import AgentInterpter
from Model.knowledge_base import knowledge_rag_base
from Model.Memory import History_Chat
import time

st.set_page_config(
    page_title="MSA-Multi-Agent-System Planner",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="assets/logo.png",
)


if "list_model" not in st.session_state:
    st.session_state["list_model"] = ["llama3","llama2"]


if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content=st.write_stream(stream_data("Hello! I'm A ***Multi-Agents System Based on Graph-Engine Built to Planing JESA Project Given Description*** . How can I help you today?")))
        ]



if "multi_task_df" not in st.session_state:
    st.session_state.multi_task_df = []


# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = False


with st.sidebar:
    st.image('logo.png', width=300)
    selected = option_menu(
        menu_title="Main Menu",
        options=["Info", "MSA Planner", "LTSM-Task-DP"],
        icons=["info-circle", "robot", "bar-chart-line-fill"],
        menu_icon="cast",
        default_index=0,
    )

# Placeholder for future LSTM-related features
if selected == "Info":
    st.markdown(
        "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
    )
    st.markdown("# Project Info")
    st.write("This project leverages a Multi-Agent System (MSA) Planner to manage tasks and strategies.")

    st.markdown("## MSA : based modeling part")
    st.markdown("May we isolate each model in a separate way to predict each part of PFE but include in UI as Selected to use the model independently. Instead of using LLM as Agent.")
    
    st.image("assets/Option1.png")
    st.markdown("**Technical Framework Used :**")
    st.markdown("- **Agent Architecture:** The system employs independent agents for specialized tasks:")
    st.markdown("    - **Planner Agent:** Analyzes project descriptions and historical data (including RAG statuses) to predict a plan for the entire project")
    st.image("assets/agents.png")



# MSA Planner Section
if selected == "MSA Planner":
    with st.sidebar:
        st.markdown("## Settings")
        model_name = st.text_input("Model", placeholder="Enter model name here...")
        temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        Delete = st.toggle("remove Agent", False)
        
        if Delete:
            Remove_model = st.text_input("Agent", placeholder="Enter model name to remove...")
            remove_model(Remove_model,st)
        if model_name:
            Add_model(model_name,st)

        on = st.toggle("Activate RAG Status", False)
        if on:
            knowledge_rag_base(st)
                
    st.markdown("# MSA Planner - Multi-Agent System")
    History_Chat(st)

    # React to user input
    if prompt := st.chat_input("Enter your query for the MSA Planner..."):
        # Display user message in chat message container
        with st.chat_message("user"):
             st.markdown(prompt)

        Agents_engine(prompt, temp, model_name,st)
           


if selected == "LTSM-Task-DP":
    list_model = ["Task-Estimator","Project-Estimator"]
    st.subheader("Prediction Task Duration (LSTM) - Coming Soon")
    st.sidebar.subheader("LSTM Estimator")

    # Sidebar selection for model
    selected_model = st.sidebar.selectbox("Selected Model", options=list_model, index=0)
   
    
    def handle_prediction(selected_model):

        if st.sidebar.button("Clear Chat History"):
            if len(st.session_state.messages) >= 0:
                st.session_state.messages.clear()

        single = st.sidebar.toggle("Single Estimation", disabled=False)
        Multi = st.sidebar.toggle("Multi Estimation", disabled=False)
        

        if single:
             Estimation_tasks_and_projects(selected_model,type_task=single,is_multi_task=False,st=st)
        
        if Multi:
             Estimation_tasks_and_projects(selected_model,type_task=Multi,is_multi_task=True,st=st)

            
        toggle_statu = False
        Analysis_dash(toggle_statu,st)

        toggle_statu_agent = False
        AgentInterpter(toggle_statu_agent,st)
        
    if selected_model:
        handle_prediction(selected_model)



