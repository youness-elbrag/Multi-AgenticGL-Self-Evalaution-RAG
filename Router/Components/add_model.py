import subprocess 
import time 

def Add_model(model_name, st):
    if model_name and model_name not in st.session_state.list_model:
                with st.status(f"Downloading model API {model_name}... ⏳", state="running", expanded=True) as status:
                    st.success(f"Pulling the model {model_name}")
                    command = f"ollama pull {model_name}"
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if process.returncode == 0:
                        time.sleep(1)
                        st.success(f"Downloaded model {model_name}")
                        st.session_state.list_model.append(model_name)
                        print(st.session_state.list_model)
                        st.session_state.model_ready = True 
                        status.update(label="Download complete!", state="complete", expanded=False)
                    else:
                        st.error(f"Failed to download model {model_name}: {stderr.decode()}")
    else:
        st.success("Model already packaged and loaded successfully.")