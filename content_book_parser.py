# content_book_parser.py

import json
from typing import List, Dict, Any

class ContentPartsParser:
    """
    Класс для парсинга частей книги из JSON-структуры.
    
    Ожидаемый формат JSON:
    {
        "content": {
            "parts": [
                {
                    "title": "...",
                    "summary": "...",
                    "key_points": [...],  # список ключевых моментов
                    "part_number": ...    # номер части
                },
                ...
            ]
        }
    }
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def parse_title(self, part: Dict[str, Any]) -> str:
        return part.get("title", "Нет заголовка")

    def parse_summary(self, part: Dict[str, Any]) -> str:
        return part.get("summary", "Нет описания")

    def parse_key_points(self, part: Dict[str, Any]) -> str:
        key_points = part.get("key_points", [])
        if isinstance(key_points, list):
            return ", ".join(str(point) for point in key_points)
        return str(key_points)

    def parse_part_number(self, part: Dict[str, Any]) -> str:
        return str(part.get("part_number", "Не указан номер"))

    def format_part(self, part: Dict[str, Any]) -> str:
        title = self.parse_title(part)
        summary = self.parse_summary(part)
        key_points = self.parse_key_points(part)
        part_number = self.parse_part_number(part)

        formatted = (
            f"<Part> {part_number}:\n"
            f"<title>: {title}\n"
            f"<summary>: {summary}\n"
            f"<key_points>: {key_points}"
        )
        return formatted

    def parse_parts(self) -> List[str]:
        parts = self.data.get("content", {}).get("parts", [])
        return [self.format_part(part) for part in parts]
    
    
class ChapterParser:
    """
    Класс для парсинга глав из файла know_map_full.json.
    
    Ожидаемый формат know_map_full.json:
    {
        "content": {
            "parts": [
                {
                    "part_number": <number>,
                    "chapters": [
                        {
                            "title": "...",
                            "summary": "...",
                            "key_points": [...],
                            "chapter_number": ...
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    }
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def parse_title(self, chapter: Dict[str, Any]) -> str:
        return chapter.get("title", "Нет заголовка")

    def parse_summary(self, chapter: Dict[str, Any]) -> str:
        return chapter.get("summary", "Нет описания")

    def parse_key_points(self, chapter: Dict[str, Any]) -> str:
        key_points = chapter.get("key_points", [])
        if isinstance(key_points, list):
            return ", ".join(str(point) for point in key_points)
        return str(key_points)

    def parse_chapter_number(self, chapter: Dict[str, Any]) -> str:
        return str(chapter.get("chapter_number", "Не указан номер"))

    def format_chapter(self, chapter: Dict[str, Any]) -> str:
        title = self.parse_title(chapter)
        summary = self.parse_summary(chapter)
        key_points = self.parse_key_points(chapter)
        chapter_number = self.parse_chapter_number(chapter)

        formatted = (
            f"<Chapter> {chapter_number}:\n"
            f"<title>: {title}\n"
            f"<summary>: {summary}\n"
            f"<key_points>: {key_points}"
        )
        return formatted

    def parse_chapters_by_part(self, selected_part: int) -> List[str]:
        """
        Находит объект part с заданным part_number и парсит все главы из него.
        """
        parts = self.data.get("content", {}).get("parts", [])
        for part in parts:
            if part.get("part_number") == selected_part:
                chapters = part.get("chapters", [])
                return [self.format_chapter(ch) for ch in chapters]
        return []
    
class SubchapterParser:
    """
    Парсинг подглав для выбранной главы в know_map_full.json.

    Ожидаемый формат (тот же know_map_full.json):
    {
        "content": {
            "parts": [
                {
                    "part_number": <number>,
                    "chapters": [
                        {
                            "chapter_number": <number>,
                            "subchapters": [
                                {
                                    "title": "...",
                                    "summary": "...",
                                    "key_points": [...],
                                    "subchapter_number": ...
                                },
                                ...
                            ],
                            ... (другие поля главы)
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    }
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def parse_title(self, subchapter: Dict[str, Any]) -> str:
        return subchapter.get("title", "Нет заголовка")

    def parse_summary(self, subchapter: Dict[str, Any]) -> str:
        return subchapter.get("summary", "Нет описания")

    def parse_key_points(self, subchapter: Dict[str, Any]) -> str:
        key_points = subchapter.get("key_points", [])
        if isinstance(key_points, list):
            return ", ".join(str(point) for point in key_points)
        return str(key_points)

    def parse_subchapter_number(self, subchapter: Dict[str, Any]) -> str:
        return str(subchapter.get("subchapter_number", "Не указан номер"))

    def format_subchapter(self, subchapter: Dict[str, Any]) -> str:
        title = self.parse_title(subchapter)
        summary = self.parse_summary(subchapter)
        key_points = self.parse_key_points(subchapter)
        subchapter_number = self.parse_subchapter_number(subchapter)
        formatted = (
            f"<Subchapter> {subchapter_number}:\n"
            f"<title>: {title}\n"
            f"<summary>: {summary}\n"
            f"<key_points>: {key_points}"
        )
        return formatted

    def parse_subchapters_by_chapter(self, selected_part: int, selected_chapter: int) -> List[str]:
        parts = self.data.get("content", {}).get("parts", [])
        for part in parts:
            if part.get("part_number") == selected_part:
                chapters = part.get("chapters", [])
                for chapter in chapters:
                    if chapter.get("chapter_number") == selected_chapter:
                        subchapters = chapter.get("subchapters", [])
                        return [self.format_subchapter(sub) for sub in subchapters]
        return []
    
    
class PageContentParser:
    """
    Парсинг страниц по выбранной подглаве.

    Сначала ищем в know_map_full.json подглаву с нужным subchapter_number,
    затем извлекаем список номеров страниц (поле pages) и по ним ищем
    содержимое в файле kniga_full_content.json.

    Ожидаемый формат know_map_full.json (для подглав):
    {
        "content": {
            "parts": [
                {
                    "part_number": ...,
                    "chapters": [
                        {
                            "chapter_number": ...,
                            "subchapters": [
                                {
                                    "subchapter_number": "<значение>",
                                    "pages": [номер_страницы, ...],
                                    ... другие поля ...
                                },
                                ...
                            ]
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    }

    Ожидаемый формат kniga_full_content.json:
    {
        "book": {
            "pages": [
                {
                    "pageNumber": <номер_страницы>,
                    "content": "Содержимое страницы"
                },
                ...
            ]
        }
    }
    """
    def __init__(self, know_map_data: Dict[str, Any], kniga_data: Dict[str, Any]):
        self.know_map_data = know_map_data
        self.kniga_data = kniga_data

    def get_pages_for_subchapter(self, selected_subchapter: str) -> List[int]:
        """
        Ищем по всему know_map_data объект подглавы с subchapter_number, равным selected_subchapter,
        и возвращаем список номеров страниц из поля pages.
        """
        parts = self.know_map_data.get("content", {}).get("parts", [])
        for part in parts:
            chapters = part.get("chapters", [])
            for chapter in chapters:
                subchapters = chapter.get("subchapters", [])
                for sub in subchapters:
                    if str(sub.get("subchapter_number")) == str(selected_subchapter):
                        return sub.get("pages", [])
        return []

    def get_page_content(self, page_numbers: List[int]) -> str:
        """
        По списку номеров страниц ищем в kniga_data все объекты страниц,
        извлекаем их поле content и объединяем в одну строку.
        """
        pages = self.kniga_data.get("book", {}).get("pages", [])
        contents = []
        for page in pages:
            if page.get("pageNumber") in page_numbers:
                contents.append(str(page.get("content", "")))
        return "\n\n".join(contents)

    def parse_final_content(self, selected_subchapter: str) -> str:
        """
        Получаем список номеров страниц для выбранной подглавы и извлекаем итоговый контент.
        """
        page_numbers = self.get_pages_for_subchapter(selected_subchapter)
        return self.get_page_content(page_numbers)
    
    
# Пример тестирования новых функций (при запуске напрямую)
if __name__ == '__main__':
    # Пример для PageContentParser
    example_know_map = {
        "content": {
            "parts": [
                {
                    "part_number": 2,
                    "chapters": [
                        {
                            "chapter_number": 2,
                            "subchapters": [
                                {
                                    "subchapter_number": "2.4.25",
                                    "pages": [101, 102, 103]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    example_kniga = {
        "book": {
            "pages": [
                {"pageNumber": 101, "content": "Содержимое страницы 101."},
                {"pageNumber": 102, "content": "Содержимое страницы 102."},
                {"pageNumber": 103, "content": "Содержимое страницы 103."},
                {"pageNumber": 104, "content": "Содержимое страницы 104."}
            ]
        }
    }
    page_parser = PageContentParser(example_know_map, example_kniga)
    final_text = page_parser.parse_final_content("2.4.25")
    print("Финальный контент по выбранной подглаве:")
    print(final_text)
    

# # Пример тестирования (при запуске напрямую)
# if __name__ == '__main__':
#     # Тест для ContentPartsParser
#     example_parts = {
#         "content": {
#             "parts": [
#                 {
#                     "title": "Введение в привычки",
#                     "summary": "Описание основ формирования привычек.",
#                     "key_points": ["Самодисциплина", "Мотивация"],
#                     "part_number": 1
#                 },
#                 {
#                     "title": "Формирование продуктивности",
#                     "summary": "Практические советы по повышению эффективности.",
#                     "key_points": ["Планирование", "Приоритеты"],
#                     "part_number": 2
#                 }
#             ]
#         }
#     }
#     cp_parser = ContentPartsParser(example_parts)
#     for part_str in cp_parser.parse_parts():
#         print(part_str)
#         print("-" * 40)

#     # Тест для ChapterParser
#     example_chapters = {
#         "content": {
#             "parts": [
#                 {
#                     "part_number": 2,
#                     "chapters": [
#                         {
#                             "title": "Глава 1. Введение",
#                             "summary": "Основы темы.",
#                             "key_points": ["Ключ 1", "Ключ 2"],
#                             "chapter_number": 1,
#                             "subchapters": []  # для примера
#                         },
#                         {
#                             "title": "Глава 2. Детали",
#                             "summary": "Углублённый анализ.",
#                             "key_points": ["Ключ A", "Ключ B"],
#                             "chapter_number": 2,
#                             "subchapters": [
#                                 {
#                                     "title": "Подглава 2.1. Базовые понятия",
#                                     "summary": "Введение в базовые концепции.",
#                                     "key_points": ["Понятие А", "Понятие Б"],
#                                     "subchapter_number": 1
#                                 },
#                                 {
#                                     "title": "Подглава 2.2. Примеры",
#                                     "summary": "Практические примеры.",
#                                     "key_points": ["Пример 1", "Пример 2"],
#                                     "subchapter_number": 2
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             ]
#         }
#     }
#     ch_parser = ChapterParser(example_chapters)
#     chapters_list = ch_parser.parse_chapters_by_part(2)
#     for chapter_str in chapters_list:
#         print(chapter_str)
#         print("-" * 40)

#     # Тест для SubchapterParser
#     subch_parser = SubchapterParser(example_chapters)
#     subchapters_list = subch_parser.parse_subchapters_by_chapter(2, 2)
#     for subch_str in subchapters_list:
#         print(subch_str)
#         print("-" * 40)
