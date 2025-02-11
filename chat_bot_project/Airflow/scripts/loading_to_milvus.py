import sys
LIBS_PATH = r'C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\libs'
sys.path.append(LIBS_PATH)

from milvus_lib import MilvusDBClient, DocumentData, CollectionConfig
from log_lib import Log
from connection import connect_to_databases

if __name__ == '__main__':
    model_url = 'http://192.168.114.62:5001/embeddings'
    LibLog = Log(*connect_to_databases(), script_name='loading_to_milvus.py')

    client = MilvusDBClient(model_url=model_url, LibLog=LibLog)
    client.connect()

    try:
        client.create_collection()
        client.create_index()

        doc = DocumentData(
            text='Sample teeext',
            embedding=[0.1]*CollectionConfig.DIMENSION,
            section='Introduction',
            subsection='Overview',
            article='AI-101'
        )

        # Insert data
        client.insert_document(doc)
        question = "Перечень специальностей"
        answers = client.search_answer(question)
        
        for i, answer in enumerate(answers, 1):
            print(f"\nРезультат #{i}:")
            print(f"Текст: {answer['text']}")
            print(f"Раздел: {answer['section']}")
            print(f"Статья: {answer['article']}")
            print(f"Схожесть: {1 - answer['distance']:.2%}")

    finally:
        client.close()