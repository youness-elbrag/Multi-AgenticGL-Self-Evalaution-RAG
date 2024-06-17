import time
import subprocess

def remove_model(remove_model,st):
    if remove_model:
            if remove_model in st.session_state.list_model:
                with st.status(f"Removing model API {remove_model}... ⏳", state="running", expanded=True) as status:
                            st.success(f"Deleting the model {remove_model}")
                            command = f"ollama rm {remove_model}"
                            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            stdout, stderr = process.communicate()
                            if process.returncode == 0:
                                time.sleep(1)
                                st.session_state.list_model.remove(remove_model)
                                st.success(f"Delete model {remove_model}")
                                st.session_state.model_ready = True 
                                status.update(label="Deleting complete!", state="complete", expanded=False)
                            else:
                                st.error(f"Failed to Delete model {remove_model}: {stderr.decode()}")
            else:
                st.success("Model already Deleted successfully.")
                    
            