import nltk

# Vocabulary dictionary of known domain terms for GovScheme NLP
VOCABULARY = [
    # Indian States and Union Territories
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Jammu and Kashmir", "Ladakh",
    # Occupations
    "student", "farmer", "agriculturist", "cultivator", "entrepreneur", "business",
    "shopkeeper", "artisan", "craftsman", "employee", "unemployed", "vendor", "hawker",
    # Categories
    "education", "scholarship", "agriculture", "farming", "housing", "business",
    "employment", "health", "healthcare", "skill", "training", "social welfare",
    # Social Categories
    "general", "obc", "sc", "st", "ews"
]

# Lowercase map for quick lookup
VOCAB_MAP = {term.lower(): term for term in VOCABULARY}

def edit_distance(str1: str, str2: str) -> int:
    """
    Computes Levenshtein edit distance between two strings using dynamic programming.
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # Deletion
                                   dp[i][j - 1],      # Insertion
                                   dp[i - 1][j - 1])  # Substitution
    return dp[m][n]

def correct_word(word: str, max_distance: int = 2) -> str:
    """
    Corrects a single word against the domain vocabulary using minimum edit distance.
    Returns original word if no close match is found.
    """
    if not word or len(word) < 3:
        return word

    word_lower = word.lower()
    
    # Direct match
    if word_lower in VOCAB_MAP:
        return VOCAB_MAP[word_lower]

    best_match = word
    min_dist = max_distance + 1

    for term_lower, original_term in VOCAB_MAP.items():
        # Quick length difference check filter
        if abs(len(term_lower) - len(word_lower)) > max_distance:
            continue
            
        dist = edit_distance(word_lower, term_lower)
        if dist < min_dist:
            min_dist = dist
            best_match = original_term

    if min_dist <= max_distance:
        return best_match
    return word

def correct_text(text: str) -> dict:
    """
    Corrects spelling mistakes in a full text string for domain keywords.
    Returns original text, corrected text, and list of corrections made.
    """
    words = text.split()
    corrected_words = []
    corrections = []

    for w in words:
        # Clean punctuation from word for correction check
        clean_w = w.strip(".,!?()[]\"'")
        corrected = correct_word(clean_w)
        if corrected.lower() != clean_w.lower() and clean_w.isalpha():
            corrections.append({"original": clean_w, "corrected": corrected, "distance": edit_distance(clean_w.lower(), corrected.lower())})
            # Preserve original casing / structure if needed, or use corrected
            corrected_words.append(w.replace(clean_w, corrected))
        else:
            corrected_words.append(w)

    return {
        "original_text": text,
        "corrected_text": " ".join(corrected_words),
        "corrections": corrections
    }
