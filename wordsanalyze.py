import re
from collections import Counter
from typing import List, Dict, Tuple

# Расширенные стоп-слова для русского языка
RUSSIAN_STOP_WORDS = {
    'и', 'в', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 
    'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 
    'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 
    'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 
    'сказал', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 
    'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'человек', 
    'чего', 'раз', 'тоже', 'себе', 'под', 'жизнь', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 
    'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 
    'чтобы', 'нее', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 
    'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 
    'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 
    'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 
    'между', 'также', 'которые', 'которых', 'которой', 'которую', 'который', 'которого', 'которым',
    'которая', 'которое', 'это', 'эти', 'как', 'для', 'при', 'что', 'чем', 'все', 'уже', 'еще',
    'или', 'так', 'его', 'где', 'там', 'как', 'под', 'над', 'без', 'про', 'при', 'кто', 'как'
}

ENGLISH_STOP_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 
    'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 
    'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 
    'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 
    'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 
    'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 
    'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 
    'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 
    'has', 'had', 'were', 'said', 'each', 'where', 'may', 'find', 'before', 'right', 'too', 'here', 
    'should', 'such', 'being', 'now', 'made', 'might', 'must', 'does', 'did', 'can', 'has', 'had'
}

def detect_language(text: str) -> str:
    """Улучшенное определение языка"""
    # Считаем только значимые символы
    cyrillic_chars = sum(1 for char in text if 'а' <= char.lower() <= 'я')
    latin_chars = sum(1 for char in text if 'a' <= char.lower() <= 'z')
    
    # Если и кириллица, и латиница присутствуют
    if cyrillic_chars > 0 and latin_chars > 0:
        return 'ru' if cyrillic_chars > latin_chars else 'en'
    elif cyrillic_chars > 0:
        return 'ru'
    elif latin_chars > 0:
        return 'en'
    else:
        return 'unknown'

def clean_text(text: str) -> str:
    """Улучшенная очистка текста"""
    # Убираем HTML теги
    text = re.sub(r'<[^>]+>', '', text)
    
    # Убираем лишние пробелы и переносы
    text = re.sub(r'\s+', ' ', text)
    
    # Убираем знаки препинания и цифры, оставляем только кириллицу, латиницу и пробелы
    text = re.sub(r'[^а-яёА-ЯЁa-zA-Z\s]', ' ', text)
    
    # Убираем множественные пробелы
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def is_valid_word(word: str, language: str, min_length: int = 4) -> bool:
    """Проверяет, является ли слово валидным для анализа"""
    if len(word) < min_length:
        return False
    
    # Проверяем, что слово содержит только нужные символы
    if language == 'ru':
        return bool(re.match(r'^[а-яё]+$', word.lower()))
    elif language == 'en':
        return bool(re.match(r'^[a-z]+$', word.lower()))
    
    return False

def get_word_frequency(text: str, top_n: int = 20, min_length: int = 4) -> List[Tuple[str, int]]:
    """Анализ частоты слов с улучшенной фильтрацией"""
    
    # Определяем язык
    language = detect_language(text)
    if language == 'unknown':
        return []
    
    stop_words = RUSSIAN_STOP_WORDS if language == 'ru' else ENGLISH_STOP_WORDS
    
    # Очищаем текст
    cleaned_text = clean_text(text)
    
    # Разбиваем на слова
    words = [word.lower().strip() for word in cleaned_text.split()]
    
    # Фильтруем слова с улучшенными критериями
    filtered_words = [
        word for word in words 
        if is_valid_word(word, language, min_length)
        and word not in stop_words
    ]
    
    # Считаем частоту
    word_freq = Counter(filtered_words)
    
    return word_freq.most_common(top_n)

def analyze_text_content(soup) -> Dict:
    """Улучшенная функция анализа контента"""
    
    # Удаляем только скрипты и стили, оставляем навигацию и заголовки
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Получаем текст
    text_content = soup.get_text()
    
    print(f"DEBUG: Первые 500 символов текста: {text_content[:500]}")
    
    # Анализируем ключевые слова
    word_frequency = get_word_frequency(text_content, top_n=20, min_length=4)
    
    if not word_frequency:
        return {
            'word_count': len(text_content.split()),
            'char_count': len(text_content),
            'top_keywords': [],
            'keyword_density': [],
            'language': 'unknown',
            'unique_words': 0
        }
    
    total_words = len(text_content.split())
    unique_words = len(set(text_content.lower().split()))
    
    # Расчет плотности для топ-10 слов
    keyword_density = []
    for word, count in word_frequency:
        density = (count / total_words) * 100 if total_words > 0 else 0
        keyword_density.append({
            'word': word,
            'count': count,
            'density': round(density, 2)
        })
    
    return {
        'word_count': total_words,
        'char_count': len(text_content),
        'top_keywords': [{'word': word, 'count': count} for word, count in word_frequency],
        'keyword_density': keyword_density,
        'language': detect_language(text_content),
        'unique_words': unique_words
    }