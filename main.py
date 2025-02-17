# main.py

import json
from gigachat_module import (
    create_client,
    get_book_part_reasoning,
    get_chapter_reasoning,
    get_subchapter_reasoning,
    get_final_answer,
    SYSTEM_PROMPT_PART,
    QUESTION_USER_PART,
    SYSTEM_PROMPT_CHAPTER,
    QUESTION_USER_CHAPTER,
    SYSTEM_PROMPT_SUBCHAPTER,
    QUESTION_USER_SUBCHAPTER,
    SYSTEM_PROMPT_FINAL,
    QUESTION_USER_FINAL
)
from content_book_parser import ContentPartsParser, ChapterParser, SubchapterParser, PageContentParser

def load_json_file(file_path: str) -> dict:
    """
    Загружает данные из JSON-файла.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_content_parts_from_file(file_path: str) -> str:
    """
    Считывает JSON, парсит данные с помощью ContentPartsParser и возвращает
    итоговую строку, объединяющую информацию по всем частям книги.
    """
    data = load_json_file(file_path)
    parser = ContentPartsParser(data)
    parts_list = parser.parse_parts()
    # Объединяем строки, разделяя двумя переводами строки
    return "\n\n".join(parts_list)

def get_chapters_content_from_file(file_path: str, selected_part: int) -> str:
    """
    Считывает и парсит данные глав из know_map_full.json по выбранной части.
    """
    data = load_json_file(file_path)
    parser = ChapterParser(data)
    chapters_list = parser.parse_chapters_by_part(selected_part)
    return "\n\n".join(chapters_list)


def get_subchapters_content_from_file(file_path: str, selected_part: int, selected_chapter: int) -> str:
    data = load_json_file(file_path)
    parser = SubchapterParser(data)
    subchapters_list = parser.parse_subchapters_by_chapter(selected_part, selected_chapter)
    return "\n\n".join(subchapters_list)



def main():
    # --- ШАГ 1: Выбор части книги ---
    # Укажите путь к вашему JSON-файлу с данными частей книги
    content_parts_file = "/Users/mask/Documents/Проеты_2025/book_team_job/data_know_map/know_map_full.json"  # Замените на реальный путь
    content_parts = get_content_parts_from_file(content_parts_file)
    
    print("Спарсенные данные (CONTENT_PARTS):")
    print(content_parts)
    print("-" * 50)
    
    # Создаем клиента для LLM (замените access_token на реальный)
    access_token = "eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.Xvq2ZNaTsXpI0AGBniXCNutqeFZEqiruL-rHTUcH_dZr4Bnu25TdSW2fwD9i-PuQ2kpEMUnJJjvRDltUAVCpNClWy4V4wyu7uLHdXGKH0m-9BOGfOlKaZwrcYCrnSeuQDHfiH2dZYSelXyYSqLmJ4K7IL0StRDFZMRwu_fvm1KGt0-tvhWEGv8c5Ti5_b5TdsQVJ_w2rEaORv6jhyHxcG06OY2w3x1YVx8oB2LlFpt2FH4KEiMqPv-6mMqdScr3hw8an53WIqQkyIZJoStcCVupQxlKRVXAbGAZDiOll6szJairuIgFI5A4Xw8QZaKxiqIv9yS8yDLQ4EcfFGwoRGw.lz7Z6eLafZyNEp7DNZ-JzA.f7AnobfePEdk2zyN91Q1sP8CopJbQ6E192M5mLIGwG_NT-_Fo0tc4y8dOgQ7-VATu5yOwbmXjsqJBGI213bjeObCzbh698UmZbJby41v11ZVcoU7WoX5ENLr5xGsD94I3VK2IJVoQuNpK3XTvror0COV5BtqNk-jOuaoD4UIiYTdcIylRUOxXTqoZlHeftMibzXRF7f9AFzE26jUEOSxsm0nw89522OiM1FzCtS-PVQcqihMVSGpqgopzq1oKjl7rS4x3nW7cnEBSwE1MSMqGXlLDs_fB-YUl7bOM6OUjCSt4fTLdDQUMYDLW-tOMKXUX0W489HpxA6l4okpF-ytbY8a44gt3Cmw5UlsInabITpquuIR2oiEpC71goZPI7QiQQhUfraXNLE3o9z7fqzsEntHVJDMb1tTvBx9Sa8RatIKJrGSTN1LxBNM0xnS6QWMq6boMIEcDSHjsik2rPQHQQQvq3zovJ8c8PnO9omDl7LyrX4fmkyo1v6nXXT9O2nSjmwcYoob45TwuKO04Om39_cV8CrHwdw3kxBpkw3QaHLU62KBzr6EuG6_J4-0lhiBxOIyjIa5FUEkvorzqOTNqoV5oaZFTw3XEap92cfhW9o14PKqZtbobxuUlFyegOxkQGLdnnPeORRi6ciL-rJ4QRjyBBuxieaoNwm69GGGW8C26fhimz13TGQ_Un_4YH75j2xDGT1hIxsJ5EoDftMxCYCRzCH5-A8ifnE1QxP5o9Q.pkt6bOl1YqhLXAlslC-x1LRrh5w81TMYpBwT5Zm-IFU"
    client = create_client(access_token)
    
    # Отправляем запрос к LLM для выбора части книги (шаг 1)
    part_reasoning = get_book_part_reasoning(client, SYSTEM_PROMPT_PART, content_parts, QUESTION_USER_PART)
    print("Результат шага 1 (выбор части):")
    print(part_reasoning)
    
    selected_part = part_reasoning.selected_part
    print(f"Выбранная часть: {selected_part}")
    print("-" * 50)
    
    # --- ШАГ 2: Выбор главы ---
    know_map_file = "/Users/mask/Documents/Проеты_2025/book_team_job/data_know_map/know_map_full.json"  # замените на реальный путь
    chapters_content = get_chapters_content_from_file(know_map_file, selected_part)
    print("Спарсенные данные (CHAPTERS_CONTENT):")
    print(chapters_content)
    print("-" * 50)
    
    chapter_reasoning = get_chapter_reasoning(client, SYSTEM_PROMPT_CHAPTER, chapters_content, QUESTION_USER_CHAPTER)
    print("Результат шага 2 (выбор главы):")
    print(chapter_reasoning)
    
    selected_chapter = chapter_reasoning.selected_chapter
    print(f"Выбранная глава: {selected_chapter}")
    print("-" * 50)
    
    # --- ШАГ 3: Выбор подглавы ---
    subchapters_content = get_subchapters_content_from_file(know_map_file, selected_part, selected_chapter)
    print("Спарсенные данные (SUBCHAPTERS_CONTENT):")
    print(subchapters_content)
    print("-" * 50)
    
    subchapter_reasoning = get_subchapter_reasoning(client, SYSTEM_PROMPT_SUBCHAPTER, subchapters_content, QUESTION_USER_SUBCHAPTER)
    print("Результат шага 3 (выбор подглавы):")
    print(subchapter_reasoning)
    
    selected_subchapter = subchapter_reasoning.selected_subchapter
    print(f"Выбранная подглава: {selected_subchapter}")
    print("-" * 50)
    
    # --- ШАГ 4: Извлечение контента страниц ---
    know_map_data = load_json_file(know_map_file)
    kniga_file = "/Users/mask/Documents/Проеты_2025/book_team_job/data_update/kniga_full_content.json"  # замените на реальный путь
    kniga_data = load_json_file(kniga_file)
    
    page_parser = PageContentParser(know_map_data, kniga_data)
    final_content = page_parser.parse_final_content(selected_subchapter)
    print("Финальный контент (извлечённый из страниц):")
    print(final_content)
    print("-" * 50)
    
    # Отправляем финальный контекст в LLM для ответа на вопрос
    final_answer = get_final_answer(client, SYSTEM_PROMPT_FINAL, final_content, QUESTION_USER_FINAL)
    print("Результат финального шага (ответ по контексту):")
    print(final_answer)

if __name__ == '__main__':
    main()
