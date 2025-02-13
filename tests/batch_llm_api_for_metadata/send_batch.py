# send_batch.py

from tests.batch_llm_api_for_metadata.test_utils import load_book_pages
from tests.batch_llm_api_for_metadata.test_batch_processor import BatchProcessor
import time
import json
import logging

def send_batch_job():
    # Инициализация процессора
    processor = BatchProcessor()
    
    # Загружаем все страницы
    pages = load_book_pages("/Users/mask/Documents/Проеты_2025/book_team_job/data_update/kniga_only_pages.json")
    
    # Создаем batch файл
    batch_file = processor.create_batch_file(pages)
    
    # Загружаем файл
    file_id = processor.upload_file(batch_file)
    
    # Создаем batch-задание
    batch_id = processor.create_batch(file_id)
    
    # Сохраняем batch_id для последующей проверки
    with open("batch_job_info.json", "w") as f:
        json.dump({
            "batch_id": batch_id,
            "file_id": file_id,
            "total_pages": len(pages)
        }, f)
    
    logging.info(f"Batch задание отправлено. ID: {batch_id}")
    logging.info("Информация о задании сохранена в batch_job_info.json")

if __name__ == "__main__":
    send_batch_job()