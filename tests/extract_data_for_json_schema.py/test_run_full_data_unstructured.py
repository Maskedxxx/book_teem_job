import os
from pathlib import Path
from typing import List
from unstructured.partition.auto import partition
from unstructured.documents.elements import Element

def process_pdf(pdf_path: str) -> List[Element]:
    """
    Обрабатывает PDF файл и извлекает из него текст.
    
    Args:
        pdf_path (str): Путь к PDF файлу
        
    Returns:
        List[Element]: Список элементов документа
        
    Raises:
        FileNotFoundError: Если файл не найден
        Exception: При ошибках обработки файла
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Файл не найден: {pdf_path}")
    
    try:
        # Извлекаем элементы из PDF
        elements = partition(filename=pdf_path)
        return elements
    except Exception as e:
        raise Exception(f"Ошибка при обработке PDF: {str(e)}")

def save_extracted_text(elements: List[Element], output_path: str) -> None:
    """
    Сохраняет извлеченный текст в файл.
    
    Args:
        elements (List[Element]): Список элементов документа
        output_path (str): Путь для сохранения результата
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for element in elements:
            f.write(str(element) + '\n')

def main():
    """
    Основная функция для демонстрации работы с PDF.
    """
    # Настраиваем пути
    base_dir = Path.cwd()
    pdf_path = base_dir / "kniga.pdf"  # Укажите имя вашего PDF файла
    output_path = base_dir / "output.txt"
    
    try:
        # Обрабатываем PDF
        print(f"Начинаем обработку файла: {pdf_path}")
        elements = process_pdf(str(pdf_path))
        
        # Сохраняем результаты
        save_extracted_text(elements, str(output_path))
        print(f"Обработка завершена. Результаты сохранены в: {output_path}")
        
        # Выводим первые несколько элементов для проверки
        print("\nПервые 5 извлеченных элементов:")
        for element in elements[:5]:
            print(f"- {str(element)[:100]}...")
            
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()