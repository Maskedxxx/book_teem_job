import json
import logging
from typing import List

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def load_book_pages(file_path: str, limit: int = None) -> List[dict]:
    """
    Загружает страницы книги из JSON файла
    limit: если указан, загружает только указанное количество страниц для тестирования
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            pages = json.load(file)
            logging.info(f"Загружено {len(pages if limit is None else pages[:limit])} страниц")
            return pages[:limit] if limit is not None else pages
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        raise