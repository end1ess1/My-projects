import re
import json
from typing import List, Dict
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

class DocumentChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.patterns = {
            'header': re.compile(r'^#{1,6}\s+(.*?)$'),
            'article': re.compile(r'^\*\*(\d+)\.\*\*(.*)'),
            'diff_block': re.compile(r'^```diff\n(.*?)\n```', re.DOTALL),
            'list_item': re.compile(r'^(\+|\-|\*)\s+(.*)')
        }
        
    def _clean_diff(self, text: str) -> str:
        return re.sub(r'^[+\-] ', '', text, flags=re.MULTILINE)

    def _process_structure(self, lines: List[str]) -> List[Dict]:
        chunks = []
        current_chunk = []
        metadata = {
            'section': 'Root',
            'subsection': None,
            'article': None
        }

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect headers
            if header_match := self.patterns['header'].match(line):
                level = line.count('#')
                title = header_match.group(1)
                if level == 2:
                    metadata['section'] = title
                    metadata['subsection'] = None
                elif level == 3:
                    metadata['subsection'] = title
                continue

            # Process articles
            if article_match := self.patterns['article'].match(line):
                metadata['article'] = article_match.group(1)
                content = article_match.group(2)
                current_chunk.append({
                    'text': content,
                    'meta': metadata.copy()
                })
                continue

            # Handle diff blocks
            if diff_match := self.patterns['diff_block'].search(line):
                cleaned = self._clean_diff(diff_match.group(1))
                current_chunk.append({
                    'text': cleaned,
                    'meta': metadata.copy()
                })
                continue

            # Add to current chunk
            current_chunk.append({
                'text': line,
                'meta': metadata.copy()
            })

            # Split chunk if exceeds size
            if len(current_chunk) >= self.chunk_size:
                chunks.extend(self._split_chunk(current_chunk))
                current_chunk = current_chunk[-self.overlap:]

        if current_chunk:
            chunks.extend(self._split_chunk(current_chunk))
            
        return chunks

    def _split_chunk(self, chunk: List[Dict]) -> List[Dict]:
        text_parts = [c['text'] for c in chunk]
        full_text = ' '.join(text_parts)
        
        chunks = []
        start = 0
        while start < len(full_text):
            end = min(start + self.chunk_size, len(full_text))
            if end < len(full_text):
                end = full_text.rfind(' ', start, end) + 1
                
            chunk_text = full_text[start:end].strip()
            if chunk_text:
                chunks.append({
                    'text': chunk_text,
                    'metadata': chunk[0]['meta']
                })
            
            start = end - self.overlap if end - self.overlap > start else end
            
        return chunks

    def chunk_document(self, file_path: str) -> List[Dict]:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        return self._process_structure(lines)

class MilvusManager:
    def __init__(self, host: str = 'localhost', port: str = '19530'):
        connections.connect(host=host, port=port)
        
        self.fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="metadata", dtype=DataType.JSON),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768)
        ]
        
        self.schema = CollectionSchema(
            fields=self.fields,
            description="Document Chunks"
        )
        
        self.collection = Collection(
            name="admission_rules",
            schema=self.schema,
            using='default'
        )

    def create_index(self):
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        
        self.collection.create_index(
            field_name="vector", 
            index_params=index_params
        )

    def insert_data(self, chunks: List[Dict], vectors: List[List[float]]):
        entities = [
            [ch['text'] for ch in chunks],
            [ch['metadata'] for ch in chunks],
            vectors
        ]
        
        self.collection.insert(entities)
        self.collection.flush()

if __name__ == "__main__":
    # 1. Чанкование документа
    chunker = DocumentChunker()
    chunks = chunker.chunk_document(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\main_prep.md")
    
    # 2. Сохранение чанков для дальнейшей обработки
    with open(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    # 3. Инициализация Milvus
    #milvus = MilvusManager()
    
    # 4. Создание индексов (выполняется один раз)
    #milvus.create_index()
    
    # 5. Генерация векторов (требуется модель эмбеддингов)
    # Здесь должен быть код для преобразования текста в векторы
    # Например, с использованием sentence-transformers
    
    # 6. Вставка данных в Milvus
    # milvus.insert_data(chunks, vectors)