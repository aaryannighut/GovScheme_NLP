import re
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Safe NLTK Resource Downloader
def ensure_nltk_resources():
    resources = [
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/stopwords', 'stopwords'),
        ('corpora/wordnet', 'wordnet'),
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng')
    ]
    for res_path, res_name in resources:
        try:
            nltk.data.find(res_path)
        except LookupError:
            try:
                nltk.download(res_name, quiet=True)
            except Exception:
                pass

ensure_nltk_resources()

# Fallback English stop words if NLTK download fails
FALLBACK_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
    "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
    'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
    'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
    'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on',
    'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

def get_stopwords():
    try:
        from nltk.corpus import stopwords
        return set(stopwords.words('english'))
    except Exception:
        return FALLBACK_STOPWORDS

def preprocess_text(text: str) -> dict:
    """
    Performs complete NLP preprocessing pipeline:
    1. Text cleaning
    2. Lowercase conversion
    3. Sentence segmentation
    4. Word tokenization
    5. Stop-word removal
    6. Stemming (PorterStemmer)
    7. Lemmatization (WordNetLemmatizer)
    """
    if not text or not isinstance(text, str):
        return {
            "raw_text": "",
            "cleaned_text": "",
            "sentences": [],
            "tokens": [],
            "filtered_tokens": [],
            "stemmed_words": [],
            "lemmatized_words": []
        }

    raw_text = text.strip()
    
    # 1. Cleaned text (preserving currency symbols and basic punctuation for entity extraction later)
    # Lowercase conversion
    cleaned_text = raw_text.lower()
    
    # 2. Sentence segmentation
    try:
        sentences = nltk.sent_tokenize(raw_text)
    except Exception:
        sentences = [s.strip() for s in re.split(r'[.!?]+', raw_text) if s.strip()]

    # 3. Word Tokenization
    try:
        raw_tokens = nltk.word_tokenize(cleaned_text)
        # Keep alphanumeric tokens
        tokens = [t for t in raw_tokens if re.match(r'^[a-zA-Z0-9]+$', t)]
    except Exception:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', cleaned_text)

    # 4. Stop-word removal
    stop_words = get_stopwords()
    filtered_tokens = [t for t in tokens if t not in stop_words]

    # 5. Stemming
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(t) for t in filtered_tokens]

    # 6. Lemmatization
    try:
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(t) for t in filtered_tokens]
    except Exception:
        lemmatized_words = filtered_tokens

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "sentences": sentences,
        "tokens": tokens,
        "filtered_tokens": filtered_tokens,
        "stemmed_words": stemmed_words,
        "lemmatized_words": lemmatized_words
    }
