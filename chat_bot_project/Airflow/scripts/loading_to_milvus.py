import sys
LIBS_PATH = r'C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\libs'
sys.path.append(LIBS_PATH)

from milvus_lib import MilvusDBClient, DocumentData, CollectionConfig
from log_lib import Log
from connection import connect_to_databases

if __name__ == '__main__':
    url = 'http://192.168.114.62:5001/embeddings'
    logging = Log(*connect_to_databases(), script_name='loading_to_milvus.py')

    client = MilvusDBClient(url, logging)
    client.connect()

    try:
        client.create_collection()
        client.create_index()

        doc = DocumentData(
            text='Sample text',
            embedding=[0.1]*CollectionConfig.DIMENSION,
            section='Introduction',
            subsection='Overview',
            article='AI-101'
        )

        # Insert data
        client.insert_document(doc)
    finally:
        client.close()