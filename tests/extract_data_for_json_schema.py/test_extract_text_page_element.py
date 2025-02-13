import os
from pathlib import Path
from typing import List, Dict
from unstructured.partition.auto import partition
from unstructured.documents.elements import Element

def process_pdf(pdf_path: str, strategy: str = "auto") -> Dict[int, List[Element]]:
    """
    Обрабатывает PDF файл и извлекает из него текст, группируя элементы по страницам.

    Args:
        pdf_path (str): Путь к PDF файлу.
        strategy (str): Стратегия партиционирования ("auto", "fast", "hi_res", "ocr_only").

    Returns:
        Dict[int, List[Element]]: Словарь, где ключ - номер страницы,
                                  значение - список элементов на этой странице.

    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: При ошибках обработки файла.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Файл не найден: {pdf_path}")

    try:
        elements = partition(filename=pdf_path, strategy=strategy)
        pages: Dict[int, List[Element]] = {}
        for element in elements:
            page_number = element.metadata.page_number
            if page_number is not None:  # Проверяем наличие номера страницы
                if page_number not in pages:
                    pages[page_number] = []
                pages[page_number].append(element)
        return pages
    except Exception as e:
        raise Exception(f"Ошибка при обработке PDF: {str(e)}")

def save_extracted_text_by_page(pages: Dict[int, List[Element]], output_dir: str, single_file: bool = False) -> None:
    """
    Сохраняет извлеченный текст, сгруппированный по страницам.

    Args:
        pages (Dict[int, List[Element]]): Словарь с элементами, сгруппированными по страницам.
        output_dir (str): Путь к директории для сохранения результатов.
        single_file (bool): Если True, сохраняет всё в один файл с разделителями страниц.
                            Если False, сохраняет каждую страницу в отдельный файл.
    """
    os.makedirs(output_dir, exist_ok=True)

    if single_file:
        output_path = os.path.join(output_dir, "combined_output.txt")
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for page_number, elements in pages.items():
                outfile.write(f"===== Страница {page_number} =====\n")
                for element in elements:
                    outfile.write(str(element.text) + '\n')
                outfile.write("\n")
        print(f"Все страницы сохранены в {output_path}")

    else:
        for page_number, elements in pages.items():
            output_path = os.path.join(output_dir, f"page_{page_number}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                for element in elements:
                    f.write(str(element.text) + '\n')  # element.text для получения только текста
            print(f"Страница {page_number} сохранена в {output_path}")


def main():
    """
    Основная функция для демонстрации работы с PDF.
    """
    base_dir = Path.cwd()
    pdf_path = base_dir / "data" / "kniga.pdf"
    output_dir = base_dir / "output_by_page"  # Другая директория
    strategy = "auto" # Можно поменять на "fast", "hi_res", или "ocr_only"

    try:
        print(f"Начинаем обработку файла: {pdf_path} со стратегией {strategy}")
        pages = process_pdf(str(pdf_path), strategy=strategy)

        # Выбираем, сохранять в один файл или в несколько
        save_extracted_text_by_page(pages, str(output_dir), single_file=True)


    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()