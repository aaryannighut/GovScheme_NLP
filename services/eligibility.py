def evaluate_scheme_eligibility(user_profile: dict, scheme: dict) -> dict:
    """
    Evaluates rule-based eligibility of a single scheme against a user profile.
    Produces per-criterion breakdown: MATCHED, NOT_MATCHED, NOT_PROVIDED, NOT_APPLICABLE.
    Calculates transparent 'Profile Match Score'.
    """
    criteria_breakdown = {}
    matched_points = 0
    total_possible_points = 0

    # 1. Age Criterion
    min_age = scheme.get("minimum_age")
    max_age = scheme.get("maximum_age")
    user_age = user_profile.get("age")

    if min_age is not None or max_age is not None:
        total_possible_points += 20
        if user_age is not None:
            if (min_age is None or user_age >= min_age) and (max_age is None or user_age <= max_age):
                criteria_breakdown["age"] = {
                    "status": "MATCHED",
                    "details": f"User age ({user_age}) is within eligible range ({min_age or 0} - {max_age or '∞'})"
                }
                matched_points += 20
            else:
                criteria_breakdown["age"] = {
                    "status": "NOT_MATCHED",
                    "details": f"User age ({user_age}) does not satisfy scheme criteria ({min_age or 0} - {max_age or '∞'})"
                }
        else:
            criteria_breakdown["age"] = {
                "status": "NOT_PROVIDED",
                "details": f"Age not provided in text (Scheme requires {min_age or 0} - {max_age or '∞'})"
            }
    else:
        criteria_breakdown["age"] = {
            "status": "NOT_APPLICABLE",
            "details": "No age restriction specified for this scheme"
        }

    # 2. Income Criterion
    max_income = scheme.get("maximum_income")
    user_income = user_profile.get("income")

    if max_income is not None:
        total_possible_points += 25
        if user_income is not None:
            if user_income <= max_income:
                criteria_breakdown["income"] = {
                    "status": "MATCHED",
                    "details": f"User income (₹{user_income:,}) is within scheme limit (≤ ₹{max_income:,})"
                }
                matched_points += 25
            else:
                criteria_breakdown["income"] = {
                    "status": "NOT_MATCHED",
                    "details": f"User income (₹{user_income:,}) exceeds maximum limit (₹{max_income:,})"
                }
        else:
            criteria_breakdown["income"] = {
                "status": "NOT_PROVIDED",
                "details": f"Income not provided in text (Scheme maximum limit: ₹{max_income:,})"
            }
    else:
        criteria_breakdown["income"] = {
            "status": "NOT_APPLICABLE",
            "details": "No upper income limit specified for this scheme"
        }

    # 3. State / Scope Criterion
    scope = scheme.get("scope", "Central")
    state_scope = scheme.get("state_scope", [])
    user_state = user_profile.get("state")

    if scope == "State" and state_scope:
        total_possible_points += 20
        if user_state:
            if user_state in state_scope:
                criteria_breakdown["state"] = {
                    "status": "MATCHED",
                    "details": f"User state ({user_state}) matches scheme state restriction ({', '.join(state_scope)})"
                }
                matched_points += 20
            else:
                criteria_breakdown["state"] = {
                    "status": "NOT_MATCHED",
                    "details": f"Scheme is restricted to {', '.join(state_scope)}, but user is from {user_state}"
                }
        else:
            criteria_breakdown["state"] = {
                "status": "NOT_PROVIDED",
                "details": f"State not specified (Scheme is restricted to {', '.join(state_scope)})"
            }
    else:
        criteria_breakdown["state"] = {
            "status": "MATCHED",
            "details": f"Central Scheme available across all Indian states/UTs (User State: {user_state or 'Any'})"
        }
        total_possible_points += 20
        matched_points += 20

    # 4. Social Category Criterion
    eligible_cats = scheme.get("eligible_categories", [])
    user_cat = user_profile.get("category")

    if eligible_cats and len(eligible_cats) < 5:  # If specific categories specified
        total_possible_points += 15
        if user_cat:
            if user_cat in eligible_cats:
                criteria_breakdown["category"] = {
                    "status": "MATCHED",
                    "details": f"User category ({user_cat}) is eligible ({', '.join(eligible_cats)})"
                }
                matched_points += 15
            else:
                criteria_breakdown["category"] = {
                    "status": "NOT_MATCHED",
                    "details": f"User category ({user_cat}) is not in eligible list ({', '.join(eligible_cats)})"
                }
        else:
            criteria_breakdown["category"] = {
                "status": "NOT_PROVIDED",
                "details": f"Social category not provided (Scheme targets: {', '.join(eligible_cats)})"
            }
    else:
        criteria_breakdown["category"] = {
            "status": "MATCHED",
            "details": "Open to all categories (General, OBC, SC, ST, EWS)"
        }
        total_possible_points += 15
        matched_points += 15

    # 5. Occupation Criterion
    eligible_occs = scheme.get("eligible_occupations", [])
    user_occ = user_profile.get("occupation")

    if eligible_occs:
        total_possible_points += 10
        if user_occ:
            if user_occ in eligible_occs:
                criteria_breakdown["occupation"] = {
                    "status": "MATCHED",
                    "details": f"User occupation ({user_occ}) matches scheme target occupation ({', '.join(eligible_occs)})"
                }
                matched_points += 10
            else:
                criteria_breakdown["occupation"] = {
                    "status": "NOT_MATCHED",
                    "details": f"User occupation ({user_occ}) does not match scheme target ({', '.join(eligible_occs)})"
                }
        else:
            criteria_breakdown["occupation"] = {
                "status": "NOT_PROVIDED",
                "details": f"Occupation not provided (Scheme targets: {', '.join(eligible_occs)})"
            }
    else:
        criteria_breakdown["occupation"] = {
            "status": "NOT_APPLICABLE",
            "details": "No specific occupation restriction"
        }

    # 6. Requirement / Need Category Criterion
    scheme_cat = scheme.get("category")
    user_need = user_profile.get("need_category")

    if user_need:
        total_possible_points += 10
        if user_need.lower() == scheme_cat.lower():
            criteria_breakdown["need"] = {
                "status": "MATCHED",
                "details": f"User need ({user_need}) aligns with scheme domain ({scheme_cat})"
            }
            matched_points += 10
        else:
            criteria_breakdown["need"] = {
                "status": "NOT_MATCHED",
                "details": f"User specified need ({user_need}) differs from scheme domain ({scheme_cat})"
            }

    # Calculate Profile Match Score percentage
    if total_possible_points > 0:
        match_score = round((matched_points / total_possible_points) * 100, 1)
    else:
        match_score = 50.0

    return {
        "scheme_id": scheme.get("id"),
        "scheme_name": scheme.get("name"),
        "profile_match_score": match_score,
        "criteria_breakdown": criteria_breakdown,
        "is_overall_matched": match_score >= 50.0
    }

def match_user_profile_with_schemes(user_profile: dict, schemes: list) -> list:
    """
    Evaluates all schemes against the extracted user profile and ranks by Profile Match Score.
    """
    evaluated_schemes = []
    for s in schemes:
        eval_res = evaluate_scheme_eligibility(user_profile, s)
        scheme_combined = dict(s)
        scheme_combined["eligibility_evaluation"] = eval_res
        scheme_combined["profile_match_score"] = eval_res["profile_match_score"]
        evaluated_schemes.append(scheme_combined)

    # Sort descending by profile match score
    evaluated_schemes.sort(key=lambda x: x["profile_match_score"], reverse=True)
    return evaluated_schemes
