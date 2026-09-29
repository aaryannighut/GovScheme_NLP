from nlp.text_similarity import TFIDFSearchEngine
from services.eligibility import evaluate_scheme_eligibility

class SchemeSearchService:
    def __init__(self, schemes: list):
        self.schemes = schemes
        self.search_engine = TFIDFSearchEngine(schemes)

    def search_schemes(self, query: str = "", category_filter: str = "All", state_filter: str = "All") -> list:
        """
        Searches schemes using TF-IDF cosine similarity and applies category/state filters.
        """
        if query and query.strip():
            results = self.search_engine.search(query.strip(), top_n=len(self.schemes))
        else:
            # If no query, return all schemes with default relevance
            results = [dict(s) for s in self.schemes]
            for r in results:
                r['search_relevance_score'] = 100.0

        # Apply category filter
        if category_filter and category_filter != "All":
            results = [s for s in results if s.get('category', '').lower() == category_filter.lower()]

        # Apply state filter
        if state_filter and state_filter != "All":
            filtered = []
            for s in results:
                scope = s.get('scope', 'Central')
                state_scope = s.get('state_scope', [])
                if scope == 'Central' or (scope == 'State' and state_filter in state_scope):
                    filtered.append(s)
            results = filtered

        return results

    def hybrid_search_and_match(self, query: str, user_profile: dict) -> list:
        """
        Combines TF-IDF search relevance score with rule-based Profile Match Score.
        Returns unified list sorted by hybrid score.
        """
        raw_search = self.search_schemes(query)

        hybrid_results = []
        for scheme in raw_search:
            text_score = scheme.get('search_relevance_score', 0.0)
            eval_res = evaluate_scheme_eligibility(user_profile, scheme)
            rule_score = eval_res['profile_match_score']

            # Weighted combination: 60% rule match, 40% text similarity
            hybrid_score = round(0.6 * rule_score + 0.4 * text_score, 1)

            scheme_combined = dict(scheme)
            scheme_combined['eligibility_evaluation'] = eval_res
            scheme_combined['profile_match_score'] = rule_score
            scheme_combined['hybrid_score'] = hybrid_score
            hybrid_results.append(scheme_combined)

        hybrid_results.sort(key=lambda x: (x['profile_match_score'], x['search_relevance_score']), reverse=True)
        return hybrid_results
