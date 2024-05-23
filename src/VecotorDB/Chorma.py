import os
from typing import List
import pandas as pd
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

os.environ["DATA"] = "./DATA/"
os.environ["LOAD"] = "./LOAD/"

class Retriever:
    """
    A class to handle retrieval of documents and related operations.
    """

    _DATA_PATH = os.getenv("DATA")
    _DATA_SQL = os.getenv("LOAD")

    def __init__(self, data_path: str = None):
        """
        Initializes the Retriever with the specified data path.

        Args:
            data_path (str, optional): The path to the data. Defaults to None.
        """
        super().__init__()
        self.embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self._private = data_path

    def store_vectors(self, documents: List[str]) -> Chroma:
        """
        Store vectors of documents in the vector store.

        Args:
            documents (List[str]): List of documents to store.

        Returns:
            Chroma: The vector store.
        """
        db = Chroma.from_documents(
            documents=documents,
            collection_name="rag-ProjectTasks",
            embedding=self.embedding,
            persist_directory=f"{Retriever._DATA_SQL}/Documents"
        )
        return db

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the specified CSV file path.

        Returns:
            pd.DataFrame: The loaded data.
        """
        data_path = Retriever._DATA_PATH
        for file in os.listdir(data_path):
            if file.endswith(".csv"):
                data = pd.read_csv(os.path.join(data_path, file))
                return data

    def remove_files(self) -> None:
        """
        Remove CSV files from the data directory.
        """
        if self._private is not None:
            data_path = Retriever._DATA_PATH
            for file in os.listdir(data_path):
                if file.endswith(".csv"):
                    os.remove(os.path.join(data_path, file))

    def remove_db(self) -> None:
        """
        Remove the vector store directory.
        """
        import shutil
        shutil.rmtree(f"{Retriever._DATA_SQL}/Documents")

    def retrieve(self, query: str, method_search: str = "mmr") -> str:
        """
        Retrieve documents based on the query.

        Args:
            query (str): The query to search for.
            method_search (str, optional): The retrieval method. Defaults to "mmr".

        Returns:
            str: The retrieved document.
        """
        retriever = vectorstore.as_retriever(search_type=method_search)
        document = retriever.invoke(query)
        return document