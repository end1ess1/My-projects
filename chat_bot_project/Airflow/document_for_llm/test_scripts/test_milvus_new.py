import re
import json
from typing import List, Dict

class SemanticChunker:
    def __init__(self, max_chunk_size: int = 500, overlap_sentences: int = 1):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap_sentences
        self.sentence_endings = re.compile(r'(?<=[.!?])\s+')
        self.structure_patterns = {
            'header': re.compile(r'^#{1,6}\s+(.*?)$'),
            'article': re.compile(r'^\*\*(\d+)\.\*\*(.*)'),
            'diff_block': re.compile(r'^```diff\n(.*?)\n```', re.DOTALL),
            'list_item': re.compile(r'^(\d+[\)\.]|\+|\-|\*)\s+')
        }

    def _split_paragraph(self, text: str) -> List[str]:
        sentences = self.sentence_endings.split(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            sent_length = len(sentence)
            if current_length + sent_length > self.max_chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = current_chunk[-self.overlap:] if self.overlap else []
                    current_length = sum(len(s) for s in current_chunk)
                
            current_chunk.append(sentence)
            current_length += sent_length

        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks

    def _process_element(self, element: Dict, metadata: Dict) -> List[Dict]:
        chunks = []
        if element['type'] == 'text':
            for chunk in self._split_paragraph(element['content']):
                chunks.append({
                    'text': chunk,
                    'metadata': metadata.copy()
                })
        elif element['type'] == 'diff':
            chunks.append({
                'text': element['content'],
                'metadata': metadata.copy()
            })
        return chunks

    def chunk_document(self, file_path: str) -> List[Dict]:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        elements = []
        current_metadata = {'section': 'Root', 'subsection': None, 'article': None}
        current_diff = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect headers
            if header_match := self.structure_patterns['header'].match(line):
                level = line.count('#')
                title = header_match.group(1)
                if level == 2:
                    current_metadata['section'] = title
                    current_metadata['subsection'] = None
                elif level == 3:
                    current_metadata['subsection'] = title
                continue

            # Process articles
            if article_match := self.structure_patterns['article'].match(line):
                current_metadata['article'] = article_match.group(1)
                elements.append({
                    'type': 'text',
                    'content': article_match.group(2).strip()
                })
                continue

            # Handle diff blocks
            if line.startswith('```diff'):
                current_diff = []
                continue
            if line == '```' and current_diff is not None:
                elements.append({
                    'type': 'diff',
                    'content': '\n'.join(current_diff)
                })
                current_diff = None
                continue
            if current_diff is not None:
                current_diff.append(line)
                continue

            # Add regular text
            elements.append({'type': 'text', 'content': line})

        # Process all elements
        chunks = []
        for el in elements:
            chunks.extend(self._process_element(el, current_metadata))

        # Post-process to merge broken items
        merged_chunks = []
        for chunk in chunks:
            if merged_chunks and (
                chunk['text'].startswith(('а)', 'б)', 'в)', '+', '-')) or 
                merged_chunks[-1]['text'].endswith((':', ';', ','))
            ):
                merged_chunks[-1]['text'] += ' ' + chunk['text']
            else:
                merged_chunks.append(chunk)

        return merged_chunks

if __name__ == "__main__":
    chunker = SemanticChunker(max_chunk_size=500)
    chunks = chunker.chunk_document(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\main_prep.md")
    
    with open(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


