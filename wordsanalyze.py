import re
from collections import Counter
from typing import List, Dict, Tuple

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

UKRAINIAN_STOP_WORDS = {
    'і', 'в', 'не', 'що', 'він', 'на', 'я', 'з', 'як', 'а', 'то', 'всі', 'вона', 'так', 'його',
    'але', 'також', 'ви', 'за', 'по', 'тільки', 'її', 'мене', 'було', 'ось', 'від', 'ще', 'ні',
    'це', 'до', 'для', 'ми', 'тебе', 'їх', 'коли', 'де', 'є', 'надо', 'вам', 'себе', 'ніхто'
}

def detect_language(text: str) -> str:
    cyrillic_chars = sum(1 for char in text if 'а' <= char.lower() <= 'я')
    latin_chars = sum(1 for char in text if 'a' <= char.lower() <= 'z')
    
    if cyrillic_chars > 0 and latin_chars > 0:
        return 'ru' if cyrillic_chars > latin_chars else 'en'
    elif cyrillic_chars > 0:
        return 'ru'
    elif latin_chars > 0:
        return 'en'
    else:
        return 'unknown'

def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'[^а-яёА-ЯЁa-zA-Z\s]', ' ', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def is_valid_word(word: str, language: str, min_length: int = 4) -> bool:
    if len(word) < min_length:
        return False
    
    if language == 'ru':
        return bool(re.match(r'^[а-яё]+$', word.lower()))
    elif language == 'en':
        return bool(re.match(r'^[a-z]+$', word.lower()))
    
    return False

def get_word_frequency(text: str, top_n: int = 50, min_length: int = 4) -> List[Tuple[str, int]]:    
    language = detect_language(text)
    if language == 'unknown':
        return []
    
    stop_words = RUSSIAN_STOP_WORDS if language == 'ru' else ENGLISH_STOP_WORDS
    
    cleaned_text = clean_text(text)
    
    words = [word.lower().strip() for word in cleaned_text.split()]
    
    filtered_words = [
        word for word in words 
        if is_valid_word(word, language, min_length)
        and word not in stop_words
    ]
    
    word_freq = Counter(filtered_words)
    
    return word_freq.most_common(top_n)

def analyze_text_content(soup) -> Dict:    
    for script in soup(["script", "style"]):
        script.decompose()
    
    text_content = soup.get_text()
    
    print(f"DEBUG: Первые 500 символов текста: {text_content[:500]}")
    
    word_frequency = get_word_frequency(text_content, top_n=50, min_length=4)
    
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