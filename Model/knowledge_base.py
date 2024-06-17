import streamlit as st 
from engine.VectorDB.Chorma import Retriever
import os

def knowledge_rag_base(st):
    st.write("Uploading New Data into RAG!")
    file = st.file_uploader(
        "Upload CSV files",
        accept_multiple_files=True,
        type=["csv", "xlsx"],
        key="file_uploader"
    )

    

    if file:
        retriever = Retriever()
        st.session_state["uploaded_files"] = file
        for f in file:
            with open(os.path.join(retriever._DATA_PATH, f.name), "wb") as f_out: 
                f_out.write(f.getbuffer())

            file_name=f.name

        file_path = os.path.join(retriever._DATA_PATH,file_name)
        get_data_file = retriever.get_documents(data_path=[file_path])
        with st.spinner(f"Loading Data into VectorDB  {file_path.split('/')[-1]}... ⏳"):
            retriever.save_vectordb_locally(get_data_file)
            st.write("Data uploaded successfully!")

    if st.button("Clear uploaded files"):
        if st.session_state["file_uploader"] is not None:
            st.session_state["file_uploader"] = None
            st.experimental_rerun()
        else:
            pass