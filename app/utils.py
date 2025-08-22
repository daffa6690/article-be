import math

def cosine_similarity(text1: str, text2: str) -> float:
    words1, words2 = text1.split(), text2.split()
    all_words = set(words1 + words2)
    vec1 = [words1.count(w) for w in all_words]
    vec2 = [words2.count(w) for w in all_words]
    dot = sum(x*y for x,y in zip(vec1, vec2))
    norm1 = math.sqrt(sum(x*x for x in vec1))
    norm2 = math.sqrt(sum(x*x for x in vec2))
    return dot / (norm1*norm2) if norm1*norm2 !=0 else 0