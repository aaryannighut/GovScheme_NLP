import nltk
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def compute_ngrams(tokens: list) -> dict:
    """
    Computes Unigrams, Bigrams, and Trigrams with frequency counts from tokens.
    """
    if not tokens:
        return {"unigrams": [], "bigrams": [], "trigrams": []}

    unigrams = tokens
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens)-1)]
    trigrams = [" ".join(tokens[i:i+3]) for i in range(len(tokens)-2)]

    def get_freq(item_list):
        freq = {}
        for item in item_list:
            freq[item] = freq.get(item, 0) + 1
        return sorted([{"phrase": k, "count": v} for k, v in freq.items()], key=lambda x: x["count"], reverse=True)

    return {
        "unigrams": get_freq(unigrams)[:10],
        "bigrams": get_freq(bigrams)[:10],
        "trigrams": get_freq(trigrams)[:10]
    }

POS_TAG_MAP = {
    'NN': 'Noun (Singular)',
    'NNS': 'Noun (Plural)',
    'NNP': 'Proper Noun',
    'NNPS': 'Proper Noun (Plural)',
    'VB': 'Verb (Base Form)',
    'VBD': 'Verb (Past Tense)',
    'VBG': 'Verb (Gerund/Present Participle)',
    'VBN': 'Verb (Past Participle)',
    'VBP': 'Verb (Non-3rd Person Singular Present)',
    'VBZ': 'Verb (3rd Person Singular Present)',
    'JJ': 'Adjective',
    'JJR': 'Adjective (Comparative)',
    'JJS': 'Adjective (Superlative)',
    'RB': 'Adverb',
    'RBR': 'Adverb (Comparative)',
    'RBS': 'Adverb (Superlative)',
    'CD': 'Cardinal Digit/Number',
    'PRP': 'Personal Pronoun',
    'IN': 'Preposition/Conjunction'
}

def get_pos_tags(tokens: list) -> list:
    """
    Returns NLTK POS tags mapped to human-understandable tag descriptions.
    """
    if not tokens:
        return []
    try:
        tagged = pos_tag(tokens)
        result = []
        for word, tag in tagged:
            category = POS_TAG_MAP.get(tag, tag)
            result.append({"word": word, "tag": tag, "category": category})
        return result
    except Exception:
        return [{"word": t, "tag": "UNK", "category": "Unknown"} for t in tokens]

def get_wordnet_info(keyword: str) -> dict:
    """
    Retrieves WordNet synsets, definitions, and synonyms for a given keyword.
    """
    if not keyword:
        return {"word": keyword, "synonyms": [], "definition": "No keyword provided"}
    
    keyword_clean = keyword.lower().strip()
    synonyms = set()
    definition = ""
    
    try:
        synsets = wn.synsets(keyword_clean)
        if synsets:
            definition = synsets[0].definition()
            for syn in synsets:
                for lemma in syn.lemmas():
                    name = lemma.name().replace('_', ' ')
                    if name.lower() != keyword_clean:
                        synonyms.add(name)
    except Exception:
        definition = "WordNet data currently unavailable."

    return {
        "word": keyword_clean,
        "definition": definition,
        "synonyms": list(synonyms)[:8]
    }

class TFIDFSearchEngine:
    """
    TF-IDF Information Retrieval engine for searching government schemes.
    """
    def __init__(self, schemes: list):
        self.schemes = schemes
        self.corpus = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._build_corpus()

    def _build_corpus(self):
        for s in self.schemes:
            # Combine fields to build search document
            text_parts = [
                s.get('name', ''),
                s.get('category', ''),
                s.get('description', ''),
                " ".join(s.get('keywords', [])),
                " ".join(s.get('target_groups', [])),
                " ".join(s.get('eligible_occupations', []))
            ]
            doc = " ".join(text_parts).lower()
            self.corpus.append(doc)
        
        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def search(self, query: str, top_n: int = 10) -> list:
        """
        Calculates cosine similarity between user query vector and scheme corpus vectors.
        Returns scheme dictionaries augmented with search_relevance_score.
        """
        if not query or not query.strip() or not self.corpus:
            return []

        query_vec = self.vectorizer.transform([query.lower()])
        cosine_sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Sort indices by highest score
        ranked_indices = cosine_sims.argsort()[::-1]

        results = []
        for idx in ranked_indices:
            score = float(cosine_sims[idx])
            if score > 0.01:  # Relevance threshold
                scheme_copy = dict(self.schemes[idx])
                scheme_copy['search_relevance_score'] = round(score * 100, 1)
                results.append(scheme_copy)

        return results[:top_n]
