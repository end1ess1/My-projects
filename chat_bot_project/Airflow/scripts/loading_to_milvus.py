import sys
LIBS_PATH = r'C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\libs'
sys.path.append(LIBS_PATH)

from milvus_lib import MilvusDBClient, DocumentData, CollectionConfig
from model_lib import Model
from log_lib import Log
from connection import connect_to_databases
import json
import os

if __name__ == '__main__':
    MODEL_URL = 'http://192.168.0.156:5001/embedding'
    LibLog = Log(*connect_to_databases(), script_name='loading_to_milvus.py')
    FOLDER = r'C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\preprocessing_documents'
    
    client = MilvusDBClient(model_url=MODEL_URL, LibLog=LibLog)
    client.connect()
    
    try:
        client.create_collection()
        client.create_index()

        # for file in os.listdir(FOLDER):
        #     if file.endswith(".json"):
        #         with open(os.path.join(FOLDER, file), "r", encoding="utf-8") as ff:
        #             data = json.load(ff)
        #     break
                
        # for info in data:
        #     doc = DocumentData(
        #         text=info['text'],
        #         embedding=Model(MODEL_URL).get_embedding(info['text']),
        #         section=info['metadata']['section'] if info['metadata']['section'] is not None else 'None',
        #         subsection=info['metadata']['subsection']  if info['metadata']['subsection'] is not None else 'None',
        #         article=info['metadata']['article']  if info['metadata']['article'] is not None else 'None'
        #     )
        #     client.insert_document(doc)
        
        doc = DocumentData(
                text='Новое',
                embedding=Model(MODEL_URL).get_embedding('text'),
                section='Новое',
                subsection='Новое',
                article='Новое'
            )
        
        client.insert_document(doc)

    finally:
        client.close()