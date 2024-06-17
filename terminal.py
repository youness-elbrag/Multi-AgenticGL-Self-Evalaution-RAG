import streamlit as st
from streamlit_ttyd import terminal
import time 

cmd = st.text_input("Command to run")
if cmd:
    # start the ttyd server and display the terminal on streamlit
    ttydprocess, port = terminal(cmd=cmd)

    # info on ttyd port
    st.text(f"ttyd server is running on port : {port}")

    # kill the ttyd server after a minute
    time.sleep(4)
    ttydprocess.kill()