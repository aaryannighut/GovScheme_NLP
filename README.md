# GOVSCHEME NLP 🇮🇳
### Smart Government Scheme Eligibility Checker Using Natural Language Processing

> **Tagline:** Describe Your Need. Discover Relevant Government Schemes.  
> **Project Type:** Engineering College Academic NLP Mini Project  

---

## 📌 1. Project Overview & Description
**GovScheme NLP** is a lightweight, web-based Natural Language Processing application designed to solve the accessibility barrier in discovering Indian government schemes. Citizens often find it difficult to navigate rigid forms or official portals. This project enables users to express their personal background (age, income, location, social category, occupation) and assistance requirements in plain, natural English prose.

Using NLP techniques (Tokenization, Lemmatization, POS Tagging, Minimum Edit Distance, Semantic Normalization, and TF-IDF Vectorization), the system automatically extracts user attributes, standardizes them, and matches them against verified scheme eligibility rules.

---

## 🎯 2. Problem Statement & Objectives
### Problem Statement:
Indian government schemes have complex eligibility criteria spread across multiple websites and documents. Citizens often miss out on welfare benefits due to technical jargon, rigid web forms, and lack of unified natural language search tools.

### Key Objectives:
1. Process unstructured natural language text input from users.
2. Extract critical demographic and financial attributes (Age, Income in INR, State, Occupation, Social Category, Requirement).
3. Apply semantic normalization and edit-distance spell correction for domain robustness.
4. Perform rule-based eligibility evaluation and calculate a transparent **Profile Match Score (%)**.
5. Provide explainable results showing matched, missing, and failed criteria alongside official portal links.

---

## ✨ 3. Features
- 🗣️ **Natural Language Input:** Accepts free-form paragraphs describing user background.
- ⚙️ **Automatic Attribute Extraction:** Regex + Dictionary + NLP entity parser extracts numerical income, age, state, category, and occupation.
- 🔤 **Edit Distance Spell Correction:** Automatically corrects typos in Indian state names, occupations, and scheme categories (e.g. `Mahrastra` ➔ `Maharashtra`, `studant` ➔ `student`).
- 🔄 **Semantic Normalization:** Maps equivalent expressions (e.g. `cultivator` ➔ `farmer`, `college student` ➔ `student`, `financial help for studies` ➔ `Education`).
- 🔎 **TF-IDF Search & Filtering:** Information retrieval using scikit-learn cosine similarity for broad keyword searches.
- 📋 **Explainable Match Results:** Displays criteria breakdown (`MATCHED`, `NOT_MATCHED`, `NOT_PROVIDED`) with green/orange/red status badges.
- 🧠 **Interactive NLP Diagnostics Page:** Dedicated viva demo view showing raw tokens, lemmatized words, POS tags, N-Grams (Bigrams/Trigrams), and WordNet semantic lookups.
- 📊 **Analytics Dashboard:** Graphical dataset distribution overview powered by Chart.js.

---

## 📚 4. NLP Concepts Implemented (Syllabus Mapping)
| Module / Concept | Implementation Details |
|---|---|
| **Sentence Segmentation & Tokenization** | `nltk.sent_tokenize` & `nltk.word_tokenize` |
| **Stop-word Removal** | NLTK english stopwords filtering |
| **Morphological Analysis** | `PorterStemmer` & `WordNetLemmatizer` |
| **Spelling Correction** | Dynamic programming Levenshtein Edit Distance (`nlp/spell_correction.py`) |
| **POS Tagging** | NLTK `pos_tag` with human-understandable tag descriptions |
| **N-Gram Analysis** | Unigrams, Bigrams, and Trigrams phrase frequency analysis |
| **Semantic Analysis / WordNet** | NLTK WordNet synsets, definitions, and synonym extraction |
| **Semantic Normalization** | Canonical mapping dictionaries (`nlp/semantic_normalization.py`) |
| **Information Retrieval** | scikit-learn `TfidfVectorizer` & Cosine Similarity (`nlp/text_similarity.py`) |
| **Named Entity Recognition (NER)** | Regex patterns + optional `spaCy` (`en_core_web_sm`) integration |

---

## 🛠️ 5. Technology Stack
- **Backend:** Python 3.13, Flask 3.0
- **NLP & Machine Learning:** NLTK, scikit-learn, spaCy
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Visualization:** Chart.js
- **Dataset:** JSON (`data/schemes.json`)

---

## 📁 6. Project Directory Structure
```
GovScheme-NLP/
│
├── app.py                      # Main Flask Web Application & Routes
├── requirements.txt            # Project Python Dependencies
├── README.md                   # Project Documentation
├── .gitignore                  # Git Ignore File
│
├── data/
│   └── schemes.json            # Curated Dataset of Verified Schemes
│
├── nlp/
│   ├── __init__.py
│   ├── preprocessing.py        # Tokenization, Lemmatization, Stemming
│   ├── entity_extraction.py    # Age, Income, State, Category Regex & NLP Parsers
│   ├── spell_correction.py     # Levenshtein Edit Distance Spelling Correction
│   ├── semantic_normalization.py # Synonyms & Canonical Entity Normalizer
│   └── text_similarity.py      # TF-IDF, POS Tagging, N-Grams, WordNet Helper
│
├── services/
│   ├── eligibility.py          # Rule-Based Eligibility Engine
│   └── scheme_search.py        # TF-IDF Search Service & Category Filtering
│
├── templates/
│   ├── base.html               # Master Layout Template
│   ├── index.html              # Home Page & Analytics Dashboard
│   ├── eligibility.html        # Text Area Input & Pre-populated Demos
│   ├── processing.html         # Animated Processing Screen Checklist
│   ├── results.html            # Matched Schemes & Extracted Profile View
│   ├── scheme_details.html     # Scheme Breakdown & Official Links
│   ├── find_schemes.html       # TF-IDF Search Engine Page
│   ├── nlp_analysis.html       # "How NLP Understands Your Input" Viva View
│   ├── how_it_works.html       # 7-Step Architecture Flow Diagram
│   ├── about.html              # About Project Page
│   └── 404.html                # Error Page
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom Government Theme CSS
│   └── js/
│       └── script.js            # Client-side Validation & Dynamic Behaviors
│
└── tests/
    ├── __init__.py
    ├── test_preprocessing.py   # Unit tests for preprocessing
    ├── test_extraction.py      # Unit tests for attribute extraction
    ├── test_eligibility.py     # Unit tests for matching engine
    └── test_search.py          # Unit tests for search & spell check
```

---

## 🚀 7. Step-by-Step Installation & Running Guide

### Step 1: Open Terminal / Command Prompt
Navigate to the project root directory:
```bash
cd c:\NLP_Project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: (Optional) Install spaCy Model
```bash
python -m spacy download en_core_web_sm
```
*(Note: If spaCy is not installed or internet is offline, the app automatically falls back gracefully to NLTK/Regex without breaking!)*

### Step 6: Run Automated Unit Tests
Verify all NLP modules:
```bash
python -m unittest discover tests
```

### Step 7: Launch the Flask Server
```bash
python app.py
```

### Step 8: Open in Web Browser
Open your browser and visit:
```
http://127.0.0.1:5000
```

---

## 💻 8. Sample Input & Output Example

### Sample Input:
> *"I am a 22 year old student from Maharashtra. My annual family income is ₹2.5 lakh. I belong to OBC category and I am looking for an education scholarship."*

### Extracted Profile Object (JSON):
```json
{
    "age": 22,
    "income": 250000,
    "state": "Maharashtra",
    "occupation": "student",
    "category": "OBC",
    "student_status": true,
    "need_category": "Education"
}
```

### Output Match Result:
- **Matched Scheme:** Post-Matric Scholarship for OBC Students
- **Profile Match Score:** `100%`
- **Criteria Breakdown:**
  - `✓ MATCHED`: Age (22) is within eligible range (15 - 30)
  - `✓ MATCHED`: Income (₹2.5 Lakh) is within scheme limit (≤ ₹2.5 Lakh)
  - `✓ MATCHED`: State Scope (Central - All States)
  - `✓ MATCHED`: Category (OBC)
  - `✓ MATCHED`: Occupation (student)

---

## 🎓 9. Viva Demonstration Guide for Students
When presenting this project to your professor:
1. **Homepage:** Show the analytics dashboard and click **Check My Eligibility**.
2. **Input:** Click the **Student Demo Example** button and submit.
3. **Processing Screen:** Explain the step-by-step checklist execution.
4. **Results Page:** Show the **Extracted User Profile** box and the **Rule Match Scores (%)** with green/orange status indicators.
5. **NLP Analysis Diagnostics Page:** Click **View NLP Diagnostics** to show:
   - Tokens & Filtered Tokens
   - Stemming vs Lemmatization
   - POS Tagging Table
   - N-Gram (Bigram/Trigram) counts
   - WordNet Synonym lookups
6. **Find Schemes Page:** Demonstrate TF-IDF Cosine Similarity search by searching `scholarship for farmers`.
7. **Code Structure:** Point out the separation of concerns: `nlp/` (preprocessing, extraction, spell correction), `services/` (matching, search), and `templates/` (UI).

---

## ⚠️ 10. Disclaimer
**GovScheme NLP is an academic prototype.** This project uses a curated dataset of schemes for educational demonstration purposes. Scheme criteria, benefits, and required documents change over time. Users must verify current guidelines on official government web portals before applying.
