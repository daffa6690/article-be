from collections import Counter

def analyze_article(article: dict):
    content = article.get('content', '').lower()
    words = content.split()
    word_count = len(words)
    
    most_common_word = Counter(words).most_common(1)
    most_common_word = most_common_word[0][0] if most_common_word else None
    
    title_clean = article.get('title', '').lower().replace(' ', '')
    is_palindrome = title_clean == title_clean[::-1]
    
    return{
        'word_count': word_count,
        'is_title_palindrome': is_palindrome,
        'most_common_word': most_common_word,
        'content': article.get('content', ''),
        'tags': article.get('tags', [])
    }