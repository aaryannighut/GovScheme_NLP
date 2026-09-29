import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

from nlp.preprocessing import preprocess_text
from nlp.entity_extraction import extract_user_profile
from nlp.spell_correction import correct_text
from nlp.semantic_normalization import normalize_occupation, normalize_need_category
from nlp.text_similarity import compute_ngrams, get_pos_tags, get_wordnet_info
from services.eligibility import match_user_profile_with_schemes, evaluate_scheme_eligibility
from services.scheme_search import SchemeSearchService

app = Flask(__name__)
app.secret_key = "govscheme_nlp_secret_key_academic_prototype"

# Load Scheme Dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "schemes.json")

def load_schemes():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading schemes.json: {e}")
        return []

SCHEMES_DATASET = load_schemes()
search_service = SchemeSearchService(SCHEMES_DATASET)

# Helper function to get analytics summary
def get_analytics_summary():
    total = len(SCHEMES_DATASET)
    categories_count = {}
    scope_count = {"Central": 0, "State": 0}

    for s in SCHEMES_DATASET:
        cat = s.get("category", "Other")
        categories_count[cat] = categories_count.get(cat, 0) + 1
        
        scope = s.get("scope", "Central")
        scope_count[scope] = scope_count.get(scope, 0) + 1

    return {
        "total_schemes": total,
        "categories": categories_count,
        "scopes": scope_count
    }

def construct_text_from_form(form):
    user_text = form.get("user_text", "").strip()
    if user_text:
        return user_text

    age = form.get("age", "").strip()
    gender = form.get("gender", "").strip()
    state = form.get("state", "").strip()
    income = form.get("income", "").strip()
    category = form.get("category", "").strip()
    occupation = form.get("occupation", "").strip()
    student_status = form.get("student_status", "").strip()
    residence = form.get("residence_type", "").strip()
    education = form.get("education_level", "").strip()
    requirement = form.get("need_category", "").strip()
    additional = form.get("additional_info", "").strip()

    sentences = []
    
    intro_parts = []
    if age:
        intro_parts.append(f"{age} year old")
    if gender and gender != "Select Gender":
        intro_parts.append(gender.lower())
    if occupation and occupation != "Select Occupation":
        intro_parts.append(occupation.lower())
    if student_status == "Yes" and "student" not in [p.lower() for p in intro_parts]:
        intro_parts.append("student")
    if education and education != "Select Education Level":
        intro_parts.append(f"({education})")
    
    s1 = "I am a " + " ".join(intro_parts) if intro_parts else "I am a citizen"
    if state and state != "Select State":
        s1 += f" from {state}"
    if residence and residence != "Select Residence Type":
        s1 += f" living in {residence} area"
    s1 += "."
    sentences.append(s1)

    if income:
        sentences.append(f"My annual family income is ₹{income}.")

    if category and category != "Select Category":
        sentences.append(f"I belong to {category} category.")

    if requirement and requirement != "Select Requirement":
        sentences.append(f"I am looking for {requirement} scheme.")

    if additional:
        sentences.append(additional)

    return " ".join(sentences)

@app.route("/")
def index():
    analytics = get_analytics_summary()
    return render_template("index.html", analytics=analytics)

@app.route("/check-eligibility", methods=["GET"])
def check_eligibility():
    return render_template("eligibility.html")

@app.route("/process-profile", methods=["POST"])
def process_profile():
    user_text = construct_text_from_form(request.form)
    if not user_text:
        return redirect(url_for("check_eligibility"))
    
    # Store text in session for analysis/results
    session["last_user_text"] = user_text
    return render_template("processing.html", user_text=user_text)

@app.route("/results", methods=["GET", "POST"])
def results():
    user_text = ""
    if request.method == "POST":
        user_text = construct_text_from_form(request.form)
    else:
        user_text = session.get("last_user_text", "")

    if not user_text:
        # Default sample text if visited directly
        user_text = "I am a 22 year old student from Maharashtra. My annual family income is ₹2.5 lakh. I belong to OBC category and I am looking for an education scholarship."


    # 1. Spelling correction
    spell_res = correct_text(user_text)
    processed_text = spell_res["corrected_text"]

    # 2. NLP Preprocessing
    nlp_prep = preprocess_text(processed_text)

    # 3. Entity & Attribute Extraction
    profile = extract_user_profile(processed_text)

    # 4. Eligibility Matching
    matched_schemes = match_user_profile_with_schemes(profile, SCHEMES_DATASET)

    # Store full analysis payload in session for NLP Analysis page
    session["nlp_analysis"] = {
        "user_text": user_text,
        "spell_correction": spell_res,
        "preprocessing": nlp_prep,
        "user_profile": profile
    }

    return render_template(
        "results.html",
        user_text=user_text,
        profile=profile,
        schemes=matched_schemes,
        spell_correction=spell_res
    )

@app.route("/scheme/<scheme_id>")
def scheme_details(scheme_id):
    scheme = next((s for s in SCHEMES_DATASET if s.get("id") == scheme_id), None)
    if not scheme:
        return render_template("404.html", message="Scheme not found"), 404

    # Evaluate against last profile if present
    nlp_data = session.get("nlp_analysis", {})
    user_profile = nlp_data.get("user_profile", extract_user_profile(""))

    evaluation = evaluate_scheme_eligibility(user_profile, scheme)

    return render_template("scheme_details.html", scheme=scheme, evaluation=evaluation, user_profile=user_profile)

@app.route("/find-schemes", methods=["GET", "POST"])
def find_schemes():
    query = request.args.get("query", "") or request.form.get("query", "")
    category = request.args.get("category", "All")
    state = request.args.get("state", "All")

    results = search_service.search_schemes(query=query, category_filter=category, state_filter=state)

    categories_list = ["All", "Education", "Agriculture", "Housing", "Business", "Health", "Skill Development", "Employment"]
    states_list = ["All", "Maharashtra", "Delhi", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Gujarat", "West Bengal"]

    return render_template(
        "find_schemes.html",
        schemes=results,
        query=query,
        selected_category=category,
        selected_state=state,
        categories=categories_list,
        states=states_list
    )

@app.route("/nlp-analysis")
def nlp_analysis():
    nlp_data = session.get("nlp_analysis")
    if not nlp_data:
        # Default analysis for viva demonstration
        default_text = "I am a 22 year old student from Maharashtra. My annual family income is ₹2.5 lakh. I belong to OBC category and I am looking for an education scholarship."
        spell_res = correct_text(default_text)
        nlp_prep = preprocess_text(default_text)
        profile = extract_user_profile(default_text)
        nlp_data = {
            "user_text": default_text,
            "spell_correction": spell_res,
            "preprocessing": nlp_prep,
            "user_profile": profile
        }

    tokens = nlp_data["preprocessing"]["tokens"]
    filtered_tokens = nlp_data["preprocessing"]["filtered_tokens"]

    ngrams = compute_ngrams(filtered_tokens)
    pos_tags = get_pos_tags(tokens)
    
    # WordNet for top keyword
    keywords = nlp_data["user_profile"].get("keywords", [])
    primary_keyword = keywords[0] if keywords else "student"
    wordnet_data = get_wordnet_info(primary_keyword)

    return render_template(
        "nlp_analysis.html",
        nlp=nlp_data,
        ngrams=ngrams,
        pos_tags=pos_tags,
        wordnet=wordnet_data
    )

@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api/analytics")
def api_analytics():
    return jsonify(get_analytics_summary())

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", message="Page Not Found"), 404

if __name__ == "__main__":
    print("=" * 60)
    print(" GOVSCHEME NLP - Smart Government Scheme Eligibility Checker")
    print(" Academic NLP Mini Project Running on http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
