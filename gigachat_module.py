# gigachat_module.py

import httpx
from pydantic import BaseModel, Field
from openai import OpenAI

# -------------------------------------------------------------------
# Схема для ответа LLM на шаг 1 (выбор части книги)
# -------------------------------------------------------------------
class BookPartReasoning(BaseModel):
    """
    Модель пошагового рассуждения для выбора релевантной части книги на основе вопроса пользователя.
    Каждое поле представляет собой определённый этап анализа для принятия обоснованного решения.
    """
    
    initial_analysis: str = Field(
        ...,
        description="""
        Общий анализ контекста и вопроса:
        - Определение ключевых слов и концепций в вопросе пользователя
        - Выделение основных тем из предоставленных частей книги
        - Формулировка того, что именно ищет пользователь
        Пример: "В вопросе пользователь интересуется концепцией наследования в Python. 
        Анализируя предоставленные части книги, вижу что материал распределён от базовых концепций 
        до продвинутых тем ООП..."
        """
    )
    
    chapter_comparison: str = Field(
        ...,
        description="""
        Детальное сравнение каждой части книги с запросом:
        - Оценка соответствия каждой части запросу пользователя
        - Выделение преимуществ и недостатков каждой части
        - Объяснение, почему одни части подходят лучше других
        Пример: "Часть 1 содержит только базовые концепции и не затрагивает наследование.
        Часть 2 полностью посвящена ООП, включая подробное объяснение наследования.
        Часть 3 содержит продвинутые примеры, но для начального понимания избыточна..."
        """
    )
    
    final_answer: str = Field(
        ...,
        description="""
        Итоговое решение с аргументацией:
        - Чёткое указание номера выбранной части
        - Основные аргументы в пользу выбора
        - Объяснение, как выбранная часть поможет решить задачу пользователя
        Пример: "Оптимальный выбор - Часть 2, так как она содержит фундаментальное объяснение 
        наследования в Python, включает необходимые примеры и построена последовательно для 
        понимания концепции. Эта часть наилучшим образом соответствует текущему запросу 
        пользователя о понимании механизма наследования."
        """
    )

    selected_part: int = Field(
        ...,
        description="Номер выбранной части книги, выберите строго один номер части от 1 до 4",
        gt=0,  
        example=2
    )
    
# -------------------------------------------------------------------
# Схема для ответа LLM на шаг 2 (выбор главы)
# -------------------------------------------------------------------
class ChapterReasoning(BaseModel):
    """
    Модель пошагового рассуждения для выбора релевантной главы внутри выбранной части книги.
    Каждое поле представляет этап анализа для принятия обоснованного решения о выборе конкретной главы.
    """
    
    preliminary_analysis: str = Field(
        ...,
        description="""
        Предварительный анализ запроса и контекста глав:
        - Выделение ключевых концепций и терминов из вопроса пользователя
        - Определение того, какие элементы нужно искать в описаниях глав
        - Формулировка критериев поиска подходящей главы
        Пример: " "preliminary_analysis": Анализируя вопрос пользователя о том, как создать свой первый веб-сайт, 
        я выделяю следующие ключевые аспекты для поиска в главах: 1) базовые концепции HTML и CSS, 
        2) структура простой веб-страницы, 3) практические шаги по созданию сайта. 
        Наиболее важным критерием является наличие пошаговых инструкций для начинающих."
        """
    )
    
    chapter_analysis: str = Field(
        ...,
        description="""
        Анализ потенциально подходящих глав:
        - Рассмотрение каждой главы на предмет соответствия запросу
        - Выделение наиболее релевантных глав
        - Объяснение, почему определенные главы подходят или не подходят
        Пример: " "chapter_analysis": В учебнике по программированию глава 2 'Основы HTML' содержит базовые концепции 
        и примеры разметки, глава 3 'CSS и стили' углубляется в оформление, а глава 4 'Создание 
        первого сайта' предоставляет пошаговое руководство. Главы 5 и 6 о JavaScript и серверной 
        части слишком сложны для начального этапа."
        """
    )
    
    final_reasoning: str = Field(
        ...,
        description="""
        Итоговое обоснование выбора конкретной главы:
        - Четкое объяснение, почему выбрана именно эта глава
        - Как содержание главы соответствует запросу пользователя
        - Какую конкретную пользу получит читатель
        Пример: " "final_reasoning": Выбираю главу 4 'Создание первого сайта', так как она идеально подходит для 
        начинающих: содержит пошаговое руководство от создания файловой структуры до публикации 
        сайта, включает базовые концепции HTML и CSS в контексте реального проекта, и предоставляет 
        готовый шаблон для практики. В отличие от глав 2 и 3, где материал подаётся более 
        теоретически, здесь все объяснения привязаны к практическому результату."
        """
    )
    
    selected_chapter: int = Field(
        ...,
        description="""Номер выбранной главы. Пример: "selected_chapter": 4""",
        gt=0,  # greater than 0
        example=4
    )    

# -------------------------------------------------------------------
# Схема для шага 3 (выбор подглавы)
# -------------------------------------------------------------------
class SubchapterReasoning(BaseModel):
    """
    Модель пошагового рассуждения для выбора релевантной подглавы внутри выбранной главы.
    Каждое поле представляет этап анализа для принятия обоснованного решения о выборе конкретной подглавы.
    """
    
    preliminary_analysis: str = Field(
        ...,
        description="""
        Предварительный анализ запроса и контекста подглав:
        - Расширение и детализация запроса пользователя
        - Определение конкретных концепций для поиска
        - Формулировка точных критериев соответствия
        Пример: "Анализируя вопрос пользователя о том, как эффективно использовать циклы в Python, 
        я ищу следующие элементы: 1) синтаксис различных типов циклов, 2) примеры применения, 
        3) типичные сценарии использования, 4) обработка исключительных случаев. Особенно важно 
        найти подглаву с практическими примерами и сравнением разных подходов."
        """
    )
    
    subchapter_analysis: str = Field(
        ...,
        description="""
        Анализ потенциально подходящих подглав:
        - Детальное рассмотрение содержания каждой подглавы
        - Оценка соответствия конкретным аспектам запроса
        - Выделение наиболее релевантных подглав с объяснением
        Пример: "Подглава 3.1 'Введение в циклы' даёт только базовые концепции. Подглава 3.2 
        'Практическое применение циклов' содержит множество примеров и сценариев использования. 
        Подглава 3.3 'Оптимизация циклов' слишком сложна для текущего запроса. Подглава 3.4 
        'Обработка ошибок' узко специализирована на исключениях."
        """
    )
    
    final_reasoning: str = Field(
        ...,
        description="""
        Итоговое обоснование выбора конкретной подглавы:
        - Аргументация выбора конкретной подглавы
        - Соответствие содержания подглавы запросу
        - Ожидаемая практическая польза для читателя
        Пример: "Выбираю подглаву 3.2 'Практическое применение циклов', так как она наилучшим 
        образом отвечает запросу пользователя. Она содержит разбор реальных сценариев 
        использования циклов, сравнение while и for, примеры с ListComprehension и советы по 
        выбору оптимального типа цикла для разных задач. В отличие от других подглав, здесь 
        теория сразу подкрепляется практикой."
        """
    )
    
    selected_subchapter: str = Field(
        ...,
        description="Номер выбранной подглавы subchapter_number которая выбрана в рассуждениях выше, которая содержит информацию для ответа, выбрать строко 1 подглаву",

    )




# -------------------------------------------------------------------
# Константы и настройки
# -------------------------------------------------------------------
GIGACHAT_BASE_URL = "https://gigachat.devices.sberbank.ru/api/v1"

# Системный промпт для шага 1 (выбор части книги)
SYSTEM_PROMPT_PART = (
    """
You are an AI assistant tasked with selecting the most relevant part of a book based on a user's question. You will receive information about book parts in the prompt_content variable and a user question. Your goal is to analyze the information and choose the most appropriate part that addresses the user's query.

    The response should strictly follow this Pydantic schema:

    class BookPartReasoning(BaseModel):
    ```Пошаговое рассуждение перед выбором части книги```
    initial_analysis: str = Field(..., description="ОПИСАНИЕ БУДЕТ ДАЛЬШЕ")
    chapter_comparison: str = Field(..., description="ОПИСАНИЕ БУДЕТ ДАЛЬШЕ")
    final_answer: str = Field(..., description="ОПИСАНИЕ БУДЕТ ДАЛЬШЕ")
    selected_part: int = Field(...,description="ОПИСАНИЕ БУДЕТ ДАЛЬШЕ",

    Here's an example of how to analyze and respond to a question:

    Content example:
    Part 1: Introduction to Python
    Summary: Covers basic Python syntax, variables, data types, and control structures.
    Part 2: Object-Oriented Programming
    Summary: Explains classes, objects, inheritance, and polymorphism in Python.

    Question example: "I want to learn how to create classes in Python. Which part should I read?"

    Response example:
    {
        "initial_analysis": "В предоставленном содержании есть две части книги. Первая часть посвящена базовым концепциям Python, а вторая часть полностью сфокусирована на объектно-ориентированном программировании, включая работу с классами.",
        
        "chapter_comparison": "Часть 1 содержит только базовые концепции и не включает материал о классах. Часть 2 напрямую отвечает на вопрос пользователя, так как полностью посвящена ООП и содержит информацию о создании и работе с классами в Python.",
        
        "final_answer": "Наиболее подходящая часть: 2. Эта часть книги специально посвящена объектно-ориентированному программированию и содержит подробное объяснение работы с классами в Python, что напрямую соответствует запросу пользователя."
        
        "selected_part": 2
    }

    To complete this task:
    1. Carefully review the provided book parts and their summaries in content_parts
    2. Analyze how each part relates to the user's question
    3. Provide your response in the exact format shown above, following the Pydantic schema

    Your response should be based solely on the information provided in the content_parts and should not include external knowledge.   
"""
)

# Системный промпт для шага 2 (выбор главы)
SYSTEM_PROMPT_CHAPTER = (
    """
        You are an AI assistant tasked with selecting the most relevant part of a book based on a user's question. You must always provide a step-by-step reasoning process following the Pydantic schema, even if you're unsure about the final selection.

        IMPORTANT INSTRUCTIONS:
        1. You MUST ALWAYS complete all reasoning steps (preliminary_analysis, chapter_analysis, final_reasoning)
        2. Only the selected_chapter field can be null, and ONLY after completing full analysis
        3. If you're unsure, use the reasoning fields to explain why, but still complete the analysis
        4. Never skip the analysis steps even if the answer seems unclear
        5. The response must always be in valid JSON format matching the Pydantic schema

        Example of correct response when uncertain:
        {
            "preliminary_analysis": "Анализируя вопрос пользователя о [тема], я определил следующие ключевые аспекты для поиска: 1)..., 2)..., 3).... Эти критерии помогут определить наличие релевантной информации в главах.",
            
            "chapter_analysis": "Рассмотрев содержание всех доступных глав: Глава 1 фокусируется на..., Глава 2 описывает..., Глава 3 содержит.... Ни одна из глав полностью не соответствует всем критериям поиска, так как...",
            
            "final_reasoning": "После тщательного анализа всех глав, я не могу однозначно выбрать конкретную главу, поскольку [подробное объяснение причин]. Информация по запросу пользователя либо распределена между несколькими главами, либо отсутствует в предоставленном содержании.",
            
            "selected_chapter": 1,
        }

        Response Schema:
        {
            "preliminary_analysis": str,  # Обязательное поле с анализом запроса
            "chapter_analysis": str,      # Обязательное поле с разбором глав
            "final_reasoning": str,       # Обязательное поле с итоговым обоснованием
            "selected_chapter": int # Номер главы после полного анализа
        }

        Remember: You must ALWAYS provide detailed reasoning in all three analysis fields, even if you ultimately cannot select a specific chapter.  
"""
)

SYSTEM_PROMPT_SUBCHAPTER = (
"""
You are an AI assistant tasked with selecting the most relevant part of a book based on a user's question. You must always provide a step-by-step reasoning process following the Pydantic schema, even if you're unsure about the final selection.

IMPORTANT INSTRUCTIONS:
1. You MUST ALWAYS complete all reasoning steps (preliminary_analysis, subchapter_analysis, final_reasoning)
2. Only the selected_chapter field can be null, and ONLY after completing full analysis
3. If you're unsure, use the reasoning fields to explain why, but still complete the analysis
4. Never skip the analysis steps even if the answer seems unclear
5. The response must always be in valid JSON format matching the Pydantic schema

Example of correct response when uncertain:
{
    "preliminary_analysis": "Анализируя вопрос пользователя о [тема], я определил следующие ключевые аспекты для поиска: 1)..., 2)..., 3).... Эти критерии помогут определить наличие релевантной информации в главах.",
    под
    "subchapter_analysis": "Рассмотрев содержание всех доступных подглав: подГлава ... фокусируется на..., подГлава .... описывает..., подГлава ... содержит.... Я считая что подглава ... вероятнее всего ответит на вопрос ... так как ... ИЛИ Ни одна из родглав полностью не соответствует всем критериям поиска, так как...",
    
    "final_reasoning": "После тщательного анализа всех подглав, я принял решение выбрать подглаву ... так как я мой предыдущий анализ выбрал подглаву ... ИЛИ я не могу однозначно выбрать конкретную подглаву, поскольку [подробное объяснение причин]. Информация по запросу пользователя либо распределена между несколькими подглавами, либо отсутствует в предоставленном содержании.",
    
    "selected_subchapter": "1.2.15"
}

Response Schema:
{
    "preliminary_analysis": str,  # Обязательное поле с анализом запроса
    "subchapter_analysis": str,      # Обязательное поле с разбором подглав
    "final_reasoning": str,       # Обязательное поле с итоговым обоснованием
    "selected_subchapter": str  # Номер подглавы после полного анализа
}

Remember: You must ALWAYS provide detailed reasoning in all three analysis fields, even if you ultimately cannot select a specific chapter.
"""
)

# Промпты для финального шага (шаг 4)
SYSTEM_PROMPT_FINAL = (
    """
Вы - опытный бизнес-консультант и эксперт по развитию управленческих навыков. Ваша задача - предоставлять подробные, структурированные ответы на вопросы пользователей, основываясь на информации из бизнес-литературы по менеджменту и лидерству.

    Принципы ответа:
    1. Начинайте с прямого ответа на вопрос
    2. Раскройте основную мысль, используя примеры из контекста
    3. Приведите практические ситуации, описанные в книге
    4. Объясните, почему это важно для руководителя
    5. Если в контексте есть конкретные рекомендации - обязательно их укажите

    Структура ответа:
    - Краткий прямой ответ на вопрос (1-2 предложения)
    - Подробное объяснение с примерами из контекста (1-2 предложение)
    - Практические выводы для руководителя (2-3 предложение)

    Тон общения:
    - Профессиональный, но дружелюбный
    - Используйте деловой язык, избегая излишней формальности
    - Говорите как опытный ментор, который делится ценными знаниями

    Важно: Ваши ответы должны быть достаточно подробными, чтобы читатель получил полное понимание темы, но при этом оставаться структурированными и понятными.
"""
)


QUESTION_USER_PART = "Какое рабочее уравнение-практику предлагает автор для работы с привычкой №20?"
QUESTION_USER_CHAPTER = "Какое рабочее уравнение-практику предлагает автор для работы с привычкой №20?"
QUESTION_USER_SUBCHAPTER = "Какое рабочее уравнение-практику предлагает автор для работы с привычкой №20?"
QUESTION_USER_FINAL = "Какое рабочее уравнение-практику предлагает автор для работы с привычкой №20?"


# -------------------------------------------------------------------
# Функции для создания клиента и получения ответа
# -------------------------------------------------------------------
def create_client(access_token: str) -> OpenAI:
    """
    Создаёт клиента OpenAI с отключенной проверкой SSL.
    """
    http_client = httpx.Client(verify=False)
    client = OpenAI(
        api_key=access_token,
        base_url=GIGACHAT_BASE_URL,
        http_client=http_client
    )
    return client

def get_book_part_reasoning(
    client: OpenAI,
    system_prompt: str,
    content_parts: str,
    question_user: str
) -> BookPartReasoning:
    """
    Отправляет запрос модели и парсит ответ в формате BookPartReasoning.
    """
    response = client.beta.chat.completions.parse(
        model="GigaChat-Max",
        temperature=0,
        messages=[
            {"role": "system", "content": f"ИНСТРУКЦИИ: {system_prompt}"},
            {"role": "user", "content": (
                f"Описания частей книги: {content_parts}\n"
                f"Вопрос пользователя: {question_user}"
            )}
        ],
        response_format=BookPartReasoning,
    )
    return response.choices[0].message.parsed

def get_chapter_reasoning(
    client: OpenAI,
    system_prompt: str,
    chapters_content: str,
    question_user: str
) -> str:
    response = client.beta.chat.completions.parse(
        model="GigaChat-Max",
        temperature=0,
        messages=[
            {"role": "system", "content": f"ИНСТРУКЦИИ: {system_prompt}"},
            {"role": "user", "content": (
                f"Описания глав выбранной части книги:\n{chapters_content}\n\nВопрос пользователя: {question_user}"
            )}
        ],
        response_format=ChapterReasoning,
    )
    return response.choices[0].message.parsed


def get_subchapter_reasoning(client: OpenAI, system_prompt: str, subchapters_content: str, question_user: str) -> SubchapterReasoning:
    response = client.beta.chat.completions.parse(
        model="GigaChat-Max",
        temperature=0,
        messages=[
            {"role": "system", "content": f"ИНСТРУКЦИИ: {system_prompt}"},
            {"role": "user", "content": f"Описания подглав выбранной главы:\n{subchapters_content}\n\nВопрос пользователя: {question_user}"}
        ],
        response_format=SubchapterReasoning,
    )
    return response.choices[0].message.parsed


def get_final_answer(client: OpenAI, system_prompt: str, final_content: str, question_user: str) -> str:
    response = client.chat.completions.create(
    model="GigaChat-Max",
    temperature = 0,
    messages=[
            {
                "role": "system",
                "content": f"ИНСТРУКЦИИ: {system_prompt}"
            },
            # Промпт оставлен пустым для дальнейшего заполнения
            {"role": "user", "content": f"""
            Контент книги который был найден ранее специальным ботом по вопрос пользователя: {final_content}
            Вопрос пользователя: {question_user}"""}
        ],
    )
    return response.choices[0].message.content


# Пример использования (для теста модуля, запускаемого напрямую)
if __name__ == '__main__':
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    client = create_client(access_token)
    
    # Шаг 1 – тестовый вызов
    CONTENT_PARTS = "<Пример контекста частей книги>"
    part_reasoning = get_book_part_reasoning(client, SYSTEM_PROMPT_PART, CONTENT_PARTS, QUESTION_USER_PART)
    print("Результат шага 1 (выбор части):")
    print(part_reasoning)
    
    # Шаг 2 – тестовый вызов
    CHAPTERS_CONTENT = "<Пример контекста глав выбранной части>"
    chapter_reasoning = get_chapter_reasoning(client, SYSTEM_PROMPT_CHAPTER, CHAPTERS_CONTENT, QUESTION_USER_CHAPTER)
    print("Результат шага 2 (выбор главы):")
    print(chapter_reasoning)
    
    # Шаг 3 – тестовый вызов
    SUBCHAPTERS_CONTENT = "<Пример контекста подглав выбранной главы>"
    subchapter_reasoning = get_subchapter_reasoning(client, SYSTEM_PROMPT_SUBCHAPTER, SUBCHAPTERS_CONTENT, QUESTION_USER_SUBCHAPTER)
    print("Результат шага 3 (выбор подглавы):")
    print(subchapter_reasoning)
    
    # Тест финального шага
    FINAL_CONTENT = "<Пример финального контента>"
    final_answer = get_final_answer(client, SYSTEM_PROMPT_FINAL, FINAL_CONTENT, QUESTION_USER_FINAL)
    print("Результат финального шага (ответ по контексту):")
    print(final_answer)
