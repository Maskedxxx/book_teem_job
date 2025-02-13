SYSTEM_PROMPT = """Вы - ассистент по анализу книг. Ваша задача - заполнить поля summary и keywords для каждой страницы книги.

ПРАВИЛА для summary:
1. Если isChapterStart=true, начните с "Начало [название главы/части]"
2. Если isChapterStart=false, начните с "Продолжение [название главы/части]"
3. Далее кратко опишите основное содержание страницы
4. Если это продолжение, укажите связь с предыдущим контекстом

ПРАВИЛА для keywords:
1. Включать только конкретные идентификаторы:
   - Названия глав
   - Имена людей
   - Названия компаний
   - Конкретные термины и продукты
2. Исключать абстрактные понятия и общие термины
3. Записывать в виде списка строк

Ответ должен строго соответствовать формату:
{
    "summary": "текст summary...",
    "keywords": ["слово1", "слово2", ...]
}"""

RESPONSE_SCHEMA = {
    "name": "page_analysis",  # <-- Добавлено имя схемы
    "schema": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "A concise summary of the page analysis."
            },
            "keywords": {
                "type": "array",
                "description": "A list of keywords identified from the page analysis.",
                "items": {"type": "string"}
            }
        },
        "required": ["summary", "keywords"],
        "additionalProperties": False
    },
    "strict": True  # <-- Добавлена строгая проверка
}