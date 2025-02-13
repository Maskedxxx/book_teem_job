import json

def add_summary_field(file_path):
    """
    Добавляет поле 'summary' в metadata каждого объекта в списке JSON из файла.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    for item in json_data:
        if "metadata" in item:
            item["metadata"]["summary"] = ""  # Оставляем пустым, чтобы заполнить позже
            item["metadata"]["keywords"] = []  # Оставляем пустым список ключевых слов

    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=2, ensure_ascii=False)

# Пример использования
file_path = "data_update/kniga_only_pages.json"
add_summary_field(file_path)
