import re
import json
from typing import List, Dict
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

class EnhancedDocumentChunker:
    def __init__(self, max_chunk_size: int = 400, overlap: int = 50):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.patterns = {
            'header': re.compile(r'^#{1,6}\s+(.*?)$'),
            'article': re.compile(r'^\*\*(\d+)\.\*\*(.*)'),
            'diff_block': re.compile(r'^```diff\n(.*?)\n```', re.DOTALL),
            'sentence_split': re.compile(r'(?<=[.!?;])\s+'),
            'list_item': re.compile(r'^(\d+[).]|[+-])\s+')
        }
        self.current_metadata = {
            'section': 'Root',
            'subsection': None,
            'article': None,
            'context': []
        }

    def _clean_diff(self, text: str) -> str:
        return '\n'.join([line[2:] for line in text.split('\n') if line.startswith('+')])

    def _update_metadata(self, line: str):
        if header_match := self.patterns['header'].match(line):
            level = line.count('#')
            title = header_match.group(1).strip()
            if level == 2:
                self.current_metadata['section'] = title
                self.current_metadata['subsection'] = None
            elif level == 3:
                self.current_metadata['subsection'] = title

        if article_match := self.patterns['article'].match(line):
            self.current_metadata['article'] = article_match.group(1)

    def _split_paragraph(self, text: str) -> List[str]:
        sentences = self.patterns['sentence_split'].split(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if current_length + len(sentence) > self.max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = current_chunk[-self.overlap:] if self.overlap else []
                current_length = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_length += len(sentence)

        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks

    def _process_element(self, element: Dict) -> List[Dict]:
        chunks = []
        content = element['content'].strip()
        
        if element['type'] == 'diff':
            cleaned = self._clean_diff(content)
            chunks.append({
                'text': cleaned,
                'metadata': self.current_metadata.copy()
            })
        else:
            for chunk in self._split_paragraph(content):
                chunks.append({
                    'text': chunk,
                    'metadata': self.current_metadata.copy()
                })
        
        return chunks

    def chunk_document(self, file_path: str) -> List[Dict]:
        elements = []
        current_diff = None

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                self._update_metadata(line)

                if line.startswith('```diff'):
                    current_diff = []
                    continue
                
                if current_diff is not None:
                    if line == '```':
                        elements.append({
                            'type': 'diff',
                            'content': '\n'.join(current_diff)
                        })
                        current_diff = None
                    else:
                        current_diff.append(line)
                    continue

                if self.patterns['article'].match(line):
                    article_num = self.patterns['article'].match(line).group(1)
                    elements.append({
                        'type': 'article',
                        'content': line,
                        'number': article_num
                    })
                else:
                    elements.append({
                        'type': 'text',
                        'content': line
                    })

        # Process elements and generate chunks
        final_chunks = []
        seen_chunks = set()
        
        for el in elements:
            for chunk in self._process_element(el):
                chunk_hash = hash(chunk['text'])
                if chunk_hash not in seen_chunks:
                    seen_chunks.add(chunk_hash)
                    final_chunks.append(chunk)

        return final_chunks

class MilvusOptimizer:
    def __init__(self):
        self.collection = None

    def connect(self, host='localhost', port='19530'):
        connections.connect(host=host, port=port)
        
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="metadata", dtype=DataType.JSON),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768)
        ]
        
        schema = CollectionSchema(
            fields=fields,
            description="Optimized Document Chunks"
        )
        
        self.collection = Collection(
            name="optimized_rules",
            schema=schema,
            using='default'
        )

    def create_index(self):
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 256}
        }
        
        self.collection.create_index(
            field_name="vector", 
            index_params=index_params
        )

    def insert_data(self, chunks: List[Dict], vectors: List[List[float]]):
        texts = [ch['text'] for ch in chunks]
        metadata = [ch['metadata'] for ch in chunks]
        
        self.collection.insert([texts, metadata, vectors])
        self.collection.flush()

if __name__ == "__main__":
    # Чанкование документа
    chunker = EnhancedDocumentChunker()
    chunks = chunker.chunk_document(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\main_prep.md")
    
    # Сохранение чанков
    with open(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\new_chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    # Подключение к Milvus
    #milvus = MilvusOptimizer()
    #milvus.connect()
    
    # Создание индекса
    #milvus.create_index()
    
    # Пример вставки данных (требуется генерация векторов)
    # vectors = generate_vectors(chunks) 
    # milvus.insert_data(chunks, vectors)