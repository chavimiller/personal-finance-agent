import re
from core.categories import load_categories, save_categories

def add_keyword_to_category(category: str, description: str):
    data = load_categories()
    category = category.strip().lower()

    keyword = re.sub(r"\d+", "", description).strip().lower()

    data.setdefault(category, [])

    if keyword not in data[category]:
        data[category].append(keyword)

    save_categories(data)

    return {
        "category" : category,
        "keyword_added" : keyword
    }

def get_categories():
    return load_categories()