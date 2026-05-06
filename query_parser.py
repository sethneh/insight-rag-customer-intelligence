import re

def parse_query(user_query: str):
    query = user_query.lower()

    filters = {
        "min_rating": None,
        "max_rating": None,
        "clean_query": user_query
    }

    # -------------------------
    # NEGATIVE SENTIMENT DETECTION
    # -------------------------
    if any(word in query for word in ["bad", "worst", "poor", "terrible", "awful"]):
        filters["max_rating"] = 2
        filters["clean_query"] = "product complaints issues problems negative feedback"

    # -------------------------
    # GOOD PRODUCTS
    # -------------------------
    elif any(word in query for word in ["good", "best", "excellent", "great"]):
        filters["min_rating"] = 4
        filters["clean_query"] = "positive reviews satisfaction praise"

    # -------------------------
    # VERY SPECIFIC PATTERN: "1 rating"
    # -------------------------
    match = re.search(r"(\d)\s*star|rating\s*(\d)", query)
    if match:
        rating = int(match.group(1) or match.group(2))
        filters["min_rating"] = rating
        filters["max_rating"] = rating

    return filters