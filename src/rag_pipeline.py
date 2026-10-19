from src.query_router import QueryRouter
from src.retriever import ProductRetriever


class RAGPipeline:

    def __init__(self, retriever=None, generator=None):

        print("Initializing RAG pipeline...")

        # Query router
        self.router = QueryRouter()

        # Product retriever
        self.retriever = retriever if retriever is not None else ProductRetriever()

        # LLM generator
        self.generator = generator

        print("RAG pipeline ready.")


    def run(self, query):

        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a nonempty string")
        query = query.strip()

        # ==========================================
        # 1. Analyze query
        # ==========================================

        analysis = self.router.analyze(
            query
        )

        intent = analysis["intent"]

        filters = analysis["filters"]

        category = filters.get(
            "category"
        )


        # ==========================================
        # 2. Cheapest product
        # ==========================================

        if intent == "cheapest":

            results = self.retriever.get_cheapest(
                category
            )

            answer = self._format_product_answer(
                results,
                "cheapest"
            )


        # ==========================================
        # 3. Most expensive product
        # ==========================================

        elif intent == "most_expensive":

            results = self.retriever.get_most_expensive(
                category
            )

            answer = self._format_product_answer(
                results,
                "most_expensive"
            )


        # ==========================================
        # 4. Category listing
        # ==========================================

        elif intent == "category_listing":

            results = self.retriever.filter_by_category(
                category
            )

            answer = self._format_category_listing(
                results,
                category
            )


        # ==========================================
        # 5. Semantic search
        # ==========================================

        elif intent == "semantic_search":

            results = self.retriever.search(
                query,
                top_k=5,
                category=category
            )

            if not results:

                answer = (
                    "I don't have enough information "
                    "to answer this."
                )

            else:

                context = "\n\n".join(
                    result["document"]
                    for result in results
                )

                if self.generator is None:
                    from src.generator import RAGGenerator
                    self.generator = RAGGenerator()

                answer = self.generator.generate(
                    query,
                    context
                )


        # ==========================================
        # 6. Unknown intent
        # ==========================================

        else:

            results = []

            answer = (
                "I don't have enough information "
                "to answer this."
            )


        # ==========================================
        # 7. Return complete result
        # ==========================================

        return {
            "query": query,
            "intent": intent,
            "filters": filters,
            "results": results,
            "answer": answer
        }


    # ==========================================
    # Structured product answer
    # ==========================================

    def _format_product_answer(
        self,
        results,
        intent
    ):

        if not results:

            return (
                "I don't have enough information "
                "to answer this."
            )


        product = results[0]

        document = product["document"]

        name = ""
        price = ""
        product_id = ""


        for line in document.splitlines():

            if line.startswith("Product ID:"):

                product_id = line.replace(
                    "Product ID:",
                    ""
                ).strip()


            elif line.startswith("Name:"):

                name = line.replace(
                    "Name:",
                    ""
                ).strip()


            elif line.startswith("Price:"):

                price = line.replace(
                    "Price:",
                    ""
                ).strip()


        if intent == "cheapest":

            return (
                f"The cheapest product is "
                f"{name} ({product_id}) at {price}."
            )


        if intent == "most_expensive":

            return (
                f"The most expensive product is "
                f"{name} ({product_id}) at {price}."
            )


        return name


    # ==========================================
    # Category listing
    # ==========================================

    def _format_category_listing(
        self,
        results,
        category
    ):

        if not results:

            return (
                "I don't have enough information "
                "to answer this."
            )


        lines = [
            f"Available {category.lower()} products:"
        ]


        for result in results:

            name = ""
            price = ""


            for line in result["document"].splitlines():

                if line.startswith("Name:"):

                    name = line.replace(
                        "Name:",
                        ""
                    ).strip()


                elif line.startswith("Price:"):

                    price = line.replace(
                        "Price:",
                        ""
                    ).strip()


            lines.append(
                f"- {name} — {price}"
            )


        return "\n".join(lines)
