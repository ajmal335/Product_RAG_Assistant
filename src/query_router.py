"""Small, explicit English router; this is not a general intent classifier."""
import re

class QueryRouter:
    CATEGORIES = {
        'gaming laptops?': 'Gaming Laptop', 'laptops?': 'Laptop',
        'smartphones?|phones?': 'Smartphone', 'headphones?': 'Headphones',
        'monitors?': 'Monitor', 'mouse|mice': 'Mouse', 'keyboards?': 'Keyboard',
        'graphics cards?': 'Graphics Card', 'processors?': 'Processor',
        'tablets?': 'Tablet', 'e-readers?': 'E-Reader',
        'power banks?': 'Power Bank', 'cameras?': 'Camera',
    }

    def analyze(self, query):
        text = ' '.join(query.casefold().split())
        filters = {}
        for pattern, category in self.CATEGORIES.items():
            if re.search(r'\b(?:' + pattern + r')\b', text):
                filters['category'] = category
                break
        if re.search(r'\b(cheapest|lowest price)\b', text):
            intent = 'cheapest'
        elif re.search(r'\b(most expensive|highest price)\b', text):
            intent = 'most_expensive'
        elif filters and re.search(r'\b(show me|list|available)\b', text):
            intent = 'category_listing'
        else:
            intent = 'semantic_search'
        return {'intent': intent, 'filters': filters}
