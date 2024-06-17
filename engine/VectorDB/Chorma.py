import os
import warnings
from typing import List, Optional
import shutil
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Set environment variables
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["CUDA_VISIBLE_DEVICES"] = "false"
os.environ["DATA"] = "engine/VectorDB//DATA/"
os.environ["LOAD"] = "engine/VectorDB//LOAD/Documents/"

class Retriever:
    """
    A class to handle retrieval of documents and related operations.
    """

    _DATA_PATH = os.getenv("DATA")
    _DATA_SQL = os.getenv("LOAD")

    def __init__(self, RAG: Optional[bool] = None):
        """
        Initializes the Retriever with the specified data path.

        Args:
            data_path (Optional[str]): The path to the data. Defaults to None.
        """
        try:
            self.embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        except RuntimeError as e:
            if "CUDA error" in str(e):
                print("CUDA is unavailable. Falling back to CPU.")
                self.embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2", device="cpu")
            else:
                raise e

        self._private = RAG

        if self._private is not None:
            self._store_db()

    def save_vectordb_locally(self, documents) -> None:
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
            persist_directory=f"{Retriever._DATA_SQL}"
        )

        # Persist the database to disk
        db.persist()

       
    def stored_vectordb_locally(self) -> Chroma:
        """
        Load the vector store from disk.

        Returns:
            Chroma: The loaded vector store.
        """
        return Chroma(
            persist_directory=f"{Retriever._DATA_SQL}",
            collection_name="rag-ProjectTasks",
            embedding_function=self.embedding
        )

    def get_documents(self,data_path = None):
        """
        Load data from the specified CSV file path.

        Returns:
            List[str]: The loaded data as a list of documents.
        """
        if data_path is None:
            data_path = Retriever._DATA_PATH
            csv_files = [os.path.join(data_path, file) for file in os.listdir(data_path) if file.endswith(".csv")]
        else:
            csv_files = data_path

        docs = [CSVLoader(url).load() for url in csv_files]
        return [item for sublist in docs for item in sublist]

    def remove_files(self) -> None:
        """
        Remove CSV files from the data directory.
        """
        if self._private:
            data_path = Retriever._DATA_PATH
            for file in os.listdir(data_path):
                if file.endswith(".csv"):
                    os.remove(file)

    def remove_db(self) -> None:
        """
        Remove the vector store directory.
        """
        shutil.rmtree(f"{Retriever._DATA_SQL}")

    @staticmethod
    def format_docs(docs) -> str:
        """
        Format documents for display.

        Args:
            docs: The documents to format.

        Returns:
            str: The formatted documents.
        """
        return "\n\n".join(doc.page_content for doc in docs)

    @classmethod
    def _store_db(cls):
        """
        Load the vector store to disk.
        """
        doc_list = cls().get_documents(data_path=None)
        cls().save_vectordb_locally(documents=doc_list)

    def invoke(self,query: str, method_search: str = "mmr"):
        """
        Retrieve documents based on the query.

        Args:
            method_search (str, optional): The retrieval method. Defaults to "mmr".

        Returns:
            str: The retrieved document.
        """
        vectorstore = self.stored_vectordb_locally()
        retriever = vectorstore.as_retriever(search_type=method_search)
        content = retriever.invoke(query)
        return content

if __name__ == "__main__":
    retriever = Retriever()
    docs =retriever.get_documents()
    retriever.save_vectordb_locally(documents=docs)
    # def retrieve(query: str):
    #     retriever = Retriever()
    #     retriever_instance = retriever.invoke(query)
    #     return retriever_instance
    # documents = retrieve("make a Planing Taks Pipeline Following this project Description : Basic Design Flexibility pipeline Baseline PHASE Phase 4 - Design")
    # print(Retriever.format_docs(documents))
