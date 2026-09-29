import re
from nlp.semantic_normalization import (
    normalize_occupation,
    normalize_need_category,
    normalize_social_category
)
from nlp.spell_correction import correct_word, edit_distance

# List of Indian States & UTs
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Chandigarh", "Puducherry",
    "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep", "Andaman and Nicobar"
]

COMMON_CITIES = [
    "Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur",
    "Delhi", "Bengaluru", "Bangalore", "Hyderabad", "Chennai", "Kolkata",
    "Ahmedabad", "Surat", "Jaipur", "Lucknow", "Kanpur", "Indore", "Bhopal",
    "Patna", "Varanasi", "Agra", "Coimbatore", "Kochi", "Visakhapatnam"
]

def extract_age(text: str) -> int:
    """
    Extracts age integer from natural language text.
    Handles: '22 years old', '22-year-old', 'age is 22', 'I am 22', 'aged 22'.
    """
    if not text:
        return None

    # Pattern 1: Explicit age phrases
    patterns = [
        r'\b(?:i\s+am|my\s+age\s+is|aged?|age\s+of)\s+(\d{1,2})\b',
        r'\b(\d{1,2})[\s-]*(?:years?|yrs?)\s*(?:old)?\b',
        r'\b(\d{1,2})\s*years?\b'
    ]

    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            age_val = int(match.group(1))
            if 5 <= age_val <= 100:  # Reasonable age bounds
                return age_val

    # Pattern 2: "I am a 22 year old" or "I am 22" (followed by student/farmer/etc or end)
    match_fallback = re.search(r'\bi\s+am\s+(\d{1,2})\b', text, re.IGNORECASE)
    if match_fallback:
        age_val = int(match_fallback.group(1))
        if 10 <= age_val <= 90:
            return age_val

    return None

def extract_income(text: str) -> int:
    """
    Extracts annual income and normalizes to INR Integer.
    Handles:
    - ₹2.5 lakh / 2.5 lakhs / 2.5 L / 2.5lakh -> 250000
    - 250000 / 2,50,000 / ₹2,50,000 -> 250000
    - 250k -> 250000
    - 3 crore -> 30000000
    - 80 thousand -> 80000
    """
    if not text:
        return None

    text_clean = text.replace(',', '')

    # Pattern 1: Lakhs / Lakh / L (e.g., 2.5 lakh, ₹2.5L, 2.5lakhs)
    match_lakh = re.search(r'(?:₹|rs\.?|inr\s*)?\s*(\d+(?:\.\d+)?)\s*(?:lakhs?|lakh|l)\b', text_clean, re.IGNORECASE)
    if match_lakh:
        amount = float(match_lakh.group(1))
        return int(amount * 100000)

    # Pattern 2: Crore / Cr (e.g., 1.5 crore, 2 cr)
    match_crore = re.search(r'(?:₹|rs\.?|inr\s*)?\s*(\d+(?:\.\d+)?)\s*(?:crores?|crore|cr)\b', text_clean, re.IGNORECASE)
    if match_crore:
        amount = float(match_crore.group(1))
        return int(amount * 10000000)

    # Pattern 3: Thousand / K (e.g., 80 thousand, 250k)
    match_k = re.search(r'(?:₹|rs\.?|inr\s*)?\s*(\d+(?:\.\d+)?)\s*(?:thousands?|thousand|k)\b', text_clean, re.IGNORECASE)
    if match_k:
        amount = float(match_k.group(1))
        return int(amount * 1000)

    # Pattern 4: Raw numeric income (e.g., income of 250000 or ₹250000)
    match_raw = re.search(r'(?:income|family\s+income|earning|salary|rs\.?|₹)\s*(?:is|=|:)?\s*(?:₹|rs\.?)?\s*(\d{5,8})\b', text_clean, re.IGNORECASE)
    if match_raw:
        return int(match_raw.group(1))

    # Fallback raw numeric number > 10000 in income context
    match_standalone = re.search(r'\b(\d{5,8})\b', text_clean)
    if match_standalone and ('income' in text_clean.lower() or 'earning' in text_clean.lower() or 'rupees' in text_clean.lower() or '₹' in text_clean):
        return int(match_standalone.group(1))

    return None

def extract_state(text: str) -> str:
    """
    Extracts Indian State or UT name from text with spelling tolerance.
    """
    if not text:
        return None

    text_lower = text.lower()

    # Direct match check
    for state in INDIAN_STATES:
        if re.search(r'\b' + re.escape(state.lower()) + r'\b', text_lower):
            return state

    # Edit distance match for typos (e.g. Mahrastra -> Maharashtra)
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    for word in words:
        if len(word) >= 5:
            for state in INDIAN_STATES:
                # Check for key target state typos
                if edit_distance(word.lower(), state.lower()) <= 2 and abs(len(word) - len(state)) <= 3:
                    return state

    return None

def extract_city(text: str) -> str:
    """Extracts city if mentioned explicitly."""
    if not text:
        return None
    text_lower = text.lower()
    for city in COMMON_CITIES:
        if re.search(r'\b' + re.escape(city.lower()) + r'\b', text_lower):
            return city
    return None

def extract_gender(text: str) -> str:
    """Extracts gender if explicitly mentioned."""
    if not text:
        return None
    text_lower = text.lower()
    if re.search(r'\b(?:female|woman|girl|lady)\b', text_lower):
        return "Female"
    elif re.search(r'\b(?:male|man|boy)\b', text_lower):
        return "Male"
    elif re.search(r'\b(?:transgender|third gender)\b', text_lower):
        return "Transgender"
    return None

def extract_rural_urban(text: str) -> str:
    """Extracts rural or urban residence status."""
    if not text:
        return None
    text_lower = text.lower()
    if re.search(r'\b(?:rural|village|gramin|panchayat)\b', text_lower):
        return "Rural"
    elif re.search(r'\b(?:urban|city|municipal|metro)\b', text_lower):
        return "Urban"
    return None

def extract_disability(text: str) -> bool:
    """Extracts disability status if explicitly mentioned."""
    if not text:
        return None
    text_lower = text.lower()
    if re.search(r'\b(?:disabled|disability|handicapped|divyang|specially abled|pwd)\b', text_lower):
        return True
    return None

def extract_marital_status(text: str) -> str:
    """Extracts marital status if explicitly mentioned."""
    if not text:
        return None
    text_lower = text.lower()
    if re.search(r'\b(?:married)\b', text_lower):
        return "Married"
    elif re.search(r'\b(?:unmarried|single)\b', text_lower):
        return "Single"
    elif re.search(r'\b(?:widow|widower)\b', text_lower):
        return "Widow"
    return None

def extract_spacy_entities(text: str) -> dict:
    """
    Safely extracts Named Entities using spaCy if available.
    """
    entities = {"PERSON": [], "GPE": [], "ORG": [], "MONEY": [], "DATE": []}
    try:
        import spacy
        try:
            nlp_spacy = spacy.load("en_core_web_sm")
            doc = nlp_spacy(text)
            for ent in doc.ents:
                if ent.label_ in entities:
                    entities[ent.label_].append(ent.text)
        except Exception:
            pass
    except ImportError:
        pass
    return entities

def extract_user_profile(text: str) -> dict:
    """
    Main attribute extraction engine combining regex, dictionaries, semantic normalization,
    and optional spaCy NER. Returns clean structured profile dictionary.
    """
    if not text or not text.strip():
        return {
            "age": None,
            "income": None,
            "state": None,
            "city": None,
            "gender": None,
            "category": None,
            "occupation": None,
            "student_status": None,
            "rural_urban": None,
            "disability": None,
            "marital_status": None,
            "need_category": None,
            "keywords": [],
            "spacy_entities": {"PERSON": [], "GPE": [], "ORG": [], "MONEY": [], "DATE": []}
        }

    raw_text = text.strip()

    age = extract_age(raw_text)
    income = extract_income(raw_text)
    state = extract_state(raw_text)
    city = extract_city(raw_text)
    gender = extract_gender(raw_text)
    category = normalize_social_category(raw_text)
    occupation = normalize_occupation(raw_text)
    need_category = normalize_need_category(raw_text)
    rural_urban = extract_rural_urban(raw_text)
    disability = extract_disability(raw_text)
    marital_status = extract_marital_status(raw_text)

    # Student status inference logic:
    student_status = None
    if occupation == "student":
        student_status = True
    elif re.search(r'\b(?:studying|college|school|university|degree|undergraduate)\b', raw_text, re.IGNORECASE):
        student_status = True
        if not occupation:
            occupation = "student"

    # Extract keywords
    words = re.findall(r'\b[a-zA-Z]{3,}\b', raw_text.lower())
    ignore_words = {'the', 'and', 'for', 'are', 'from', 'with', 'have', 'this', 'that', 'year', 'old', 'year-old', 'belong', 'looking', 'need'}
    keywords = list(dict.fromkeys([w for w in words if w not in ignore_words]))[:10]

    spacy_ents = extract_spacy_entities(raw_text)

    return {
        "age": age,
        "income": income,
        "state": state,
        "city": city,
        "gender": gender,
        "category": category,
        "occupation": occupation,
        "student_status": student_status,
        "rural_urban": rural_urban,
        "disability": disability,
        "marital_status": marital_status,
        "need_category": need_category,
        "keywords": keywords,
        "spacy_entities": spacy_ents
    }
