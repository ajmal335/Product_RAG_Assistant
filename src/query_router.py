class QueryRouter:

    def analyze(self, query):

        query_lower = query.casefold()

        filters = {}


        # ==========================================
        # Detect product category
        # ==========================================

        categories = [
            "laptop",
            "smartphone",
            "headphones",
            "monitor",
            "mouse",
            "keyboard",
            "graphics card",
            "processor",
            "tablet",
            "e-reader",
            "power bank",
            "camera"
        ]


        for category in categories:

            if category in query_lower:

                filters["category"] = category.title()

                break


        # ==========================================
        # Detect intent
        # ==========================================

        if "cheapest" in query_lower:

            intent = "cheapest"

        elif "most expensive" in query_lower:

            intent = "most_expensive"

        elif "lowest price" in query_lower:

            intent = "cheapest"

        elif "highest price" in query_lower:

            intent = "most_expensive"

        elif (
            "show me" in query_lower
            or "list" in query_lower
            or "available" in query_lower
            or query_lower.startswith("i need")
        ):

            intent = "category_listing"

        else:

            intent = "semantic_search"


        # ==========================================
        # Return query analysis
        # ==========================================

        return {
            "intent": intent,
            "filters": filters
        }