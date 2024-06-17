from engine.AgentTasks.TaskEstimator import TaskEstimator
from engine.AgentTasks.Estimator import TaskDurationEstimator
from engine.AgentTasks.Tokenizer import Tokenizer
from engine.AgentTasks.ProjectEstimator import ProjectEstimator
import os 
import streamlit as st
from Model.Memory import History_Memory ,History_Chat

os.environ["TASK"] = "engine/AgentTasks/checkpoints/TaskEstimator.pth"
os.environ["PROJECT"] = "engine/AgentTasks/checkpoints/ProjectEstimator.pth"
model_Tokenzier = "google-bert/bert-base-uncased"
tokenizer =Tokenizer(model_Tokenzier)

def run_model(model_name, prompt, task_estimator, is_multi_task=False):
    if model_name in ["Task-Estimator", "Project-Estimator"]:
        if is_multi_task:
            # Split prompt into tasks based on new lines, ignoring leading and trailing whitespaces
            tasks = [task.strip() for task in prompt.split("\n") if task.strip()]
            return task_estimator.multi_task_durations(tasks)
        else:
            return task_estimator.single_task_duration(prompt.strip())  # Strip leading and trailing whitespaces
    return None


def Estimator(model_name, min_total_hours=None, max_total_hours=None, model_tokenizer=None,st=st):
    if model_tokenizer is None:
        st.error("Model tokenizer is required.")

    if model_name not in ["Task-Estimator", "Project-Estimator"]:
        st.error("Invalid model name. Supported options: 'Task-Estimator', 'Project-Estimator'.")

    model_cls = TaskEstimator if model_name == "Task-Estimator" else ProjectEstimator

    task_estimator = TaskDurationEstimator(model_cls, model_tokenizer, min_total_hours=min_total_hours, max_total_hours=max_total_hours)

    model_path_env = os.getenv("TASK" if model_name == "Task-Estimator" else "PROJECT")
    if model_path_env is None:
         st.error(f"Environment variable for {model_name} model path is not set.")

    task_estimator.load_model(model_path_env)

    return task_estimator



def Estimation_tasks_and_projects(model_name,type_task,is_multi_task,st):
    st.subheader(f"{model_name} - {type_task} Estimation")
    min_total_hours = st.number_input("Insert a min_total_hours", value=1.0, placeholder="Type a estimation...")
    max_total_hours = st.number_input("Insert a max_total_hours", value=33869.0, placeholder="Type a estimation...")
    task_estimator =Estimator(model_name,min_total_hours,max_total_hours,tokenizer,st)

    # Display chat messages from history on app rerun
    History_Chat(st)
    
    
    if task_prompt := st.chat_input(f"Enter a single task description for {model_name}..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(task_prompt)

        with st.spinner("Processing your request..."):
            task_df = run_model(model_name, task_prompt, task_estimator,is_multi_task=is_multi_task)
            if task_df is not None:
                response = task_df.to_markdown(index=False)
                with st.chat_message("assistant"):
                    st.write(response)
                    
                st.session_state.multi_task_df.append(task_df)
                History_Memory(task_prompt,response,st)

            else:
                st.error("Model is not available. Please wait for the download to complete.")



