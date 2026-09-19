import faiss
import pandas as pd

from sentence_transformers import SentenceTransformer


class ProductRetriever:

    def __init__(
        self,
        data_path="data/products.csv",
        model_name="all-MiniLM-L6-v2"
    ):

        # ==========================================
        # Load dataset
        # ==========================================

        self.df = pd.read_csv(
            data_path
        )


        # ==========================================
        # Load embedding model
        # ==========================================

        self.model = SentenceTransformer(
            model_name
        )


        # ==========================================
        # Create product documents
        # ==========================================

        self.documents = []

        for _, row in self.df.iterrows():

            document = f"""
Product ID: {row['productid']}
Name: {row['name']}
Category: {row['category']}
Description: {row['description']}
Stock: {row['stock']}
Season: {row['season']}
Price: ${row['price']}
""".strip()

            self.documents.append(
                document
            )


        # ==========================================
        # Generate embeddings
        # ==========================================

        embeddings = self.model.encode(
            self.documents
        ).astype("float32")


        # ==========================================
        # Normalize embeddings
        # ==========================================

        faiss.normalize_L2(
            embeddings
        )


        # ==========================================
        # Create FAISS index
        # ==========================================

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )


        # ==========================================
        # Add embeddings to index
        # ==========================================

        self.index.add(
            embeddings
        )


    # ==========================================
    # Semantic Search
    # ==========================================

    def search(
        self,
        query,
        top_k=5,
        category=None,
        min_score=0.25
    ):

        # Generate query embedding
        query_embedding = self.model.encode(
            [query]
        ).astype("float32")


        # Normalize query embedding
        faiss.normalize_L2(
            query_embedding
        )


        # Search all documents so that
        # category filtering can be applied
        search_k = len(
            self.documents
        )

        scores, indices = self.index.search(
            query_embedding,
            search_k
        )


        results = []


        for score, index in zip(
            scores[0],
            indices[0]
        ):

            # ======================================
            # Category filter
            # ======================================

            if category is not None:

                product_category = str(
                    self.df.iloc[index]["category"]
                ).casefold()

                if product_category != category.casefold():

                    continue


            # ======================================
            # Similarity threshold
            # ======================================

            if score < min_score:

                continue


            # ======================================
            # Add result
            # ======================================

            results.append(
                {
                    "document": self.documents[index],
                    "score": float(score),
                    "product_id": self.df.iloc[index]["productid"]
                }
            )


            if len(results) >= top_k:

                break


        return results


    # ==========================================
    # Filter by Category
    # ==========================================

    def filter_by_category(
        self,
        category
    ):

        if category is None:

            return []


        filtered = self.df[
            self.df["category"].astype(str).str.casefold()
            == category.casefold()
        ]


        results = []


        for _, row in filtered.iterrows():

            results.append(
                self._row_to_result(
                    row
                )
            )


        return results


    # ==========================================
    # Cheapest Product
    # ==========================================

    def get_cheapest(
        self,
        category=None
    ):

        df = self.df


        if category is not None:

            df = df[
                df["category"].astype(str).str.casefold()
                == category.casefold()
            ]


        if df.empty:

            return []


        row = df.loc[
            df["price"].idxmin()
        ]


        return [
            self._row_to_result(
                row
            )
        ]


    # ==========================================
    # Most Expensive Product
    # ==========================================

    def get_most_expensive(
        self,
        category=None
    ):

        df = self.df


        if category is not None:

            df = df[
                df["category"].astype(str).str.casefold()
                == category.casefold()
            ]


        if df.empty:

            return []


        row = df.loc[
            df["price"].idxmax()
        ]


        return [
            self._row_to_result(
                row
            )
        ]


    # ==========================================
    # Convert DataFrame Row
    # ==========================================

    def _row_to_result(
        self,
        row
    ):

        index = row.name


        return {
            "document": self.documents[index],
            "score": None,
            "product_id": row["productid"]
        }