# check_results.py
from tests.batch_llm_api_for_metadata.test_batch_processor import BatchProcessor
import json
import logging

def check_and_save_results():
    try:
        # Загружаем информацию о batch-задании
        with open("batch_job_info.json", "r") as f:
            job_info = json.load(f)
            
        processor = BatchProcessor()
        batch_id = job_info["batch_id"]
        
        # Получаем полную информацию о batch
        batch = processor.client.batches.retrieve(batch_id)
        status = batch.status
        print(f"Текущий статус: {status}")
        
        if status == "failed":
            if batch.error_file_id:
                # Получаем содержимое файла с ошибками
                error_content = processor.client.files.content(batch.error_file_id)
                print("\nДетали ошибок:")
                print(error_content.text)
            else:
                print("\nОбщая информация о batch:")
                print(f"Errors: {batch.errors}")
                print(f"Request counts: {batch.request_counts}")
                
        elif status == "completed":
            # Получаем результаты
            batch = processor.client.batches.retrieve(batch_id)
            results = processor.get_results(batch)
            
            if results:
                # Сохраняем результаты в файл
                with open("batch_results.json", "w", encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print("Результаты сохранены в batch_results.json")
                
                # Выводим краткую статистику
                print(f"Обработано страниц: {len(results)}")
                errors = [r for r in results if r.get('error')]
                if errors:
                    print(f"Количество ошибок: {len(errors)}")
        
        return status, batch
            
    except FileNotFoundError:
        print("Файл batch_job_info.json не найден. Сначала запустите send_batch.py")
    except Exception as e:
        logging.error(f"Ошибка при проверке результатов: {e}")
        raise

if __name__ == "__main__":
    check_and_save_results()