# test_batch.py
from tests.batch_llm_api_for_metadata.test_utils import load_book_pages
from tests.batch_llm_api_for_metadata.test_batch_processor import BatchProcessor
import time
import json
import logging

def test_batch_processing():
    # Инициализация процессора
    processor = BatchProcessor()
    
    # Загружаем тестовые страницы (первые 2)
    pages = load_book_pages("/Users/mask/Documents/Проеты_2025/book_team_job/data_update/kniga_only_pages.json", limit=2)
    
    # Создаем batch файл
    batch_file = processor.create_batch_file(pages)
    
    # Загружаем файл
    file_id = processor.upload_file(batch_file)
    
    # Создаем batch-задание
    batch_id = processor.create_batch(file_id)
    
    # Проверяем статус каждые 30 секунд
    while True:
        status = processor.check_status(batch_id)
        if status == "completed":
            batch = processor.client.batches.retrieve(batch_id)
            logging.info(f"Batch завершен. output_file_id: {batch.output_file_id}")
            
            results = processor.get_results(batch)
            if results:
                for result in results:
                    print(f"\nРезультат для {result['custom_id']}:")
                    print(f"Ответ: {json.dumps(result['response'], ensure_ascii=False, indent=2)}")
                    if result['error']:
                        print(f"Ошибка: {result['error']}")
            break
        elif status in ["failed", "expired", "cancelled"]:
            print(f"Задание завершилось со статусом: {status}")
            break
        else:
            print(f"Текущий статус: {status}")
            time.sleep(30)

if __name__ == "__main__":
    test_batch_processing()