import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

from dotenv import load_dotenv
from rich.traceback import install
from tqdm import tqdm
from pydantic import ValidationError

load_dotenv()
install(show_locals=True)
sys.path.append(os.getenv("LIBS_PATH_LOCAL"))

from connection import connect_to_databases
from milvus_lib import MilvusDBClient, DocumentData
from model_lib import Model
from log_lib import Log


def _get_doc(lib_log: Log, data: Dict[str, str]) -> DocumentData:
    try:
        doc_data = DocumentData(
            text=data["text"],
            embedding=Model().get_embedding(data["text"]),
            section=data["metadata"].get("section", "None"),
            subsection=data["metadata"].get("subsection", "None"),
            article=data["metadata"].get("article", "None"),
        )
        return DocumentData(**doc_data.dict())
    except ValidationError as e:
        lib_log.error(f"Data validation error: {e}")


def get_docs_list(folder: str) -> List[Dict[str, str]]:
    data = []

    for file in os.listdir(folder)[:2]:
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as ff:
                data.extend(json.load(ff))

    return data


def load_to_milvus(
    collection_name: str,
    dimension: str,
    text_len: int,
    script_name: str,
    data: List[Dict[str, str]],
) -> None:
    client = None
    LibLog = Log(*connect_to_databases(), script_name=script_name)

    try:
        client = MilvusDBClient(LibLog=LibLog)
        client.connect()
        client.create_collection(
            name=collection_name, dimension=dimension, text_len=text_len
        )
        client.create_index()

        for doc in tqdm(data):
            client.insert_document(_get_doc(LibLog, doc))

    except Exception as e:
        LibLog.error(f"Error occurred: {e}", exc_info=True)
    finally:
        if client:
            client.close()


def main():
    FOLDER = os.getenv("DOCS_FOLDER_LOCAL")
    DATA = get_docs_list(FOLDER)
    MAX_TEXT_LENGTH = max([len(i["text"]) for i in DATA])
    EMBEDDING_DIMENSION = len(Model().get_embedding("get len embedding"))

    load_to_milvus(
        collection_name="MyDocs",
        dimension=EMBEDDING_DIMENSION,
        text_len=MAX_TEXT_LENGTH,
        script_name="loading_to_milvus.py",
        data=DATA,
    )


if __name__ == "__main__":
    main()
