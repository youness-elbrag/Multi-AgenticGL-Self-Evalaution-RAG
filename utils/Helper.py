import re
import subprocess
import time

def extract_code_from_output(text):
    text = text.replace("Python", "python")
    patterns = [r"```Python(.*?)```", r"```python(.*?)```"]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "No code found."

def execute_extracted_code(text,st):
    code = extract_code_from_output(text)
    if code != "No code found.":
        if "st.plotly_chart" in code:
            try:
                exec("")
            except Exception as e:
                st.error(f"Error executing code: {e}")
        else:
            return st.error(f"the code not Executubel Version not warm with plotly_chart")
    else:
        return st.error(f"the code not Executubel {code}")

def extract_pip_from_output(text):
    text = text.replace("Shell", "shell").replace("bash", "shell").replace("Bash", "shell")
    patterns = [r"```shell(.*?)```", r"```shell(.*?)```"]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "No code found."

def execute_pip_code(text , st):
    cmd = extract_pip_from_output(text)
    print(cmd)
    package = cmd.split(" ")[-1]
    if cmd != "No code found.":
        if cmd.startswith("pip install"):
            st.warning("Installing packages with the following command:")
            try:
                with st.status(f"Installation Package  {package}... ⏳", state="running", expanded=True) as status:
                    result = subprocess.run(cmd, shell=True,check=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        time.sleep(1)
                        st.success(f"Installed model {package}")
                        st.success(result.stdout)
                        #st.session_state.model_ready = True 
                        status.update(label="Installation complete!", state="complete", expanded=False)
                    else:
                        st.error(f"Failed to download model {package}: {stderr.decode()}")
        
            except subprocess.CalledProcessError as e:
                st.error(f"Error:{e}")
            
        else:
            return st.error(f"the command not Executabel {cmd}")

    else:
         return st.error(f"the command not Executabel {cmd}")


def check_shell(out):
    if "shell" in out.lower() or "Shell" in out.lower():
        return True
    else:
        return False

def stream_data(generate):
    for word in generate.split(" "):
        yield word + " "
        time.sleep(0.02)


