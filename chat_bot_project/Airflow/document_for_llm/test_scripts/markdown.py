# **Особенности разметки:**
# 1. Использована семантическая иерархия заголовков (H1-H6)
# 2. Сохранена оригинальная нумерация пунктов
# 3. Добавлены визуальные элементы для таблиц, блоков кода и списков
# 4. Выделены ключевые нормативные требования
# 5. Реализована адаптивная структура для разных типов контента

# **Скрипт для автоматизации обработки:**

import re
from pathlib import Path

def parse_document(text: str) -> dict:
    structure = {
        'sections': [],
        'current_section': None
    }
    
    # Регулярные выражения для элементов структуры
    patterns = {
        'main_title': r'^ПРАВИЛА ПРИЕМА\s*$',
        'chapter': r'^(?P<num>[IVXLCDM]+)\.(?P<title>.*?)$',
        'article': r'^(?P<num>\d+)\.\s?(?P<content>.*?)$',
        'subpoint': r'^(?P<marker>[а-я]\)|\d+\))\s?(?P<content>.*?)$'
    }

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue

        # Обработка глав
        if match := re.match(patterns['chapter'], line):
            structure['sections'].append({
                'type': 'chapter',
                'number': match.group('num'),
                'title': match.group('title').strip(),
                'articles': []
            })
            structure['current_section'] = structure['sections'][-1]
        
        # Обработка статей
        elif match := re.match(patterns['article'], line):
            article = {
                'number': match.group('num'),
                'content': [match.group('content')],
                'subpoints': []
            }
            if structure['current_section']:
                structure['current_section']['articles'].append(article)
        
        # Обработка подпунктов
        elif match := re.match(patterns['subpoint'], line):
            if structure['current_section'] and structure['current_section']['articles']:
                structure['current_section']['articles'][-1]['subpoints'].append({
                    'marker': match.group('marker'),
                    'content': match.group('content')
                })
        
        # Добавление текста к последнему элементу
        else:
            if structure['current_section'] and structure['current_section']['articles']:
                structure['current_section']['articles'][-1]['content'].append(line)

    return structure

def generate_markdown(data: dict, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as md_file:
        # Заголовок документа
        md_file.write("# ПРАВИЛА ПРИЕМА\n\n")
        
        # Обработка секций
        for section in data['sections']:
            md_file.write(f"## {section['number']}. {section['title']}\n\n")
            
            for article in section['articles']:
                md_file.write(f"**{article['number']}.** {' '.join(article['content'])}\n")
                
                if article['subpoints']:
                    md_file.write("\n```diff\n")
                    for sub in article['subpoints']:
                        md_file.write(f"+ {sub['marker']} {sub['content']}\n")
                    md_file.write("```\n\n")

if __name__ == "__main__":
    input_file = Path(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\main.txt")
    output_file = Path(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\main_prep.md")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    parsed = parse_document(text)
    generate_markdown(parsed, output_file)
    print(f"Документ успешно преобразован: {output_file}")