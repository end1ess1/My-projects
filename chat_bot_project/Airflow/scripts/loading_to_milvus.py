import json
import os
import sys

from connection import connect_to_databases
from dotenv import load_dotenv
from rich.traceback import install

load_dotenv()
install(show_locals=True)
sys.path.append(os.getenv("LIBS_PATH"))
from milvus_lib import MilvusDBClient, DocumentData
from model_lib import Model
from log_lib import Log


if __name__ == "__main__":
    LibLog = Log(*connect_to_databases(), script_name="loading_to_milvus.py")
    FOLDER = r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\preprocessing_documents"

    client = MilvusDBClient(LibLog=LibLog)
    client.connect()

    try:
        client.create_collection(name="test", dimension=3072)
        client.create_index()

        for file in os.listdir(FOLDER):
            if file.endswith(".json"):
                with open(os.path.join(FOLDER, file), "r", encoding="utf-8") as ff:
                    data = json.load(ff)
            break

        for info in data:
            doc = DocumentData(
                text=info["text"],
                embedding=Model().get_embedding(info["text"]),
                section=(
                    info["metadata"]["section"]
                    if info["metadata"]["section"] is not None
                    else "None"
                ),
                subsection=(
                    info["metadata"]["subsection"]
                    if info["metadata"]["subsection"] is not None
                    else "None"
                ),
                article=(
                    info["metadata"]["article"]
                    if info["metadata"]["article"] is not None
                    else "None"
                ),
            )
            client.insert_document(doc)
    finally:
        client.close()
