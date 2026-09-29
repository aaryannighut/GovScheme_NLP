# Semantic Normalization Dictionary for GovScheme NLP

OCCUPATION_MAP = {
    "student": [
        "student", "college student", "learner", "undergraduate", "postgraduate",
        "pursuing degree", "studying in college", "studying in school", "pupil",
        "scholar", "studying", "study"
    ],
    "farmer": [
        "farmer", "agriculturist", "cultivator", "kisan", "farm worker",
        "agriculture worker", "grower", "tiller"
    ],
    "entrepreneur": [
        "entrepreneur", "business owner", "startup founder", "shopkeeper",
        "self employed", "trader", "vendor", "micro enterprise", "small business owner"
    ],
    "employee": [
        "employee", "working professional", "salaried person", "private employee",
        "job holder", "salaried"
    ],
    "unemployed": [
        "unemployed", "job seeker", "without job", "seeking work", "jobless"
    ],
    "artisan": [
        "artisan", "craftsman", "traditional worker", "tailor", "carpenter", "potter", "blacksmith"
    ]
}

NEED_CATEGORY_MAP = {
    "Education": [
        "education", "scholarship", "financial help for studies", "college fees",
        "education financial assistance", "studies", "higher education", "school fee",
        "tuition", "study loan", "education loan", "degree fee"
    ],
    "Agriculture": [
        "agriculture", "farming", "money for farming", "agricultural assistance",
        "crop support", "farming subsidy", "fertilizer loan", "kisan support",
        "crop insurance", "farming aid"
    ],
    "Housing": [
        "housing", "house", "housing assistance", "home loan", "house construction",
        "pucca house", "shelter", "home subsidy", "residential aid"
    ],
    "Business": [
        "business", "entrepreneurship", "help to start a business", "business support",
        "small business loan", "startup funding", "shop loan", "micro finance", "business loan"
    ],
    "Health": [
        "health", "healthcare", "medical aid", "health insurance", "hospital bill support",
        "treatment help", "medical insurance", "hospitalization"
    ],
    "Skill Development": [
        "skill development", "skill training", "vocational training", "job training",
        "kaushal", "skill certification", "skill course"
    ],
    "Employment": [
        "employment", "job", "job assistance", "employment scheme", "apprenticeship",
        "stipend scheme", "work training"
    ]
}

CATEGORY_SOCIAL_MAP = {
    "OBC": ["obc", "other backward class", "other backward category"],
    "SC": ["sc", "scheduled caste"],
    "ST": ["st", "scheduled tribe"],
    "EWS": ["ews", "economically weaker section"],
    "General": ["general", "gen", "open category"]
}

def normalize_occupation(text: str) -> str:
    """Normalizes occupation phrases to canonical terms."""
    if not text:
        return None
    text_lower = text.lower()
    for canonical, synonyms in OCCUPATION_MAP.items():
        for syn in synonyms:
            if syn in text_lower:
                return canonical
    return None

def normalize_need_category(text: str) -> str:
    """Normalizes requirement/need expressions to standard scheme categories."""
    if not text:
        return None
    text_lower = text.lower()
    for canonical, synonyms in NEED_CATEGORY_MAP.items():
        for syn in synonyms:
            if syn in text_lower:
                return canonical
    return None

def normalize_social_category(text: str) -> str:
    """Normalizes explicitly stated social categories."""
    if not text:
        return None
    text_lower = text.lower()
    for canonical, synonyms in CATEGORY_SOCIAL_MAP.items():
        for syn in synonyms:
            # Match word boundary to avoid false positives
            import re
            pattern = r'\b' + re.escape(syn) + r'\b'
            if re.search(pattern, text_lower):
                return canonical
    return None
