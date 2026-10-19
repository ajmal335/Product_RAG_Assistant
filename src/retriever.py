"""Exact catalog operations plus lazily initialized semantic retrieval."""
from pathlib import Path
import pandas as pd

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / 'data' / 'products.csv'

class ProductRetriever:
    def __init__(self, data_path=DEFAULT_CATALOG, model_name='all-MiniLM-L6-v2'):
        self.df = pd.read_csv(data_path).reset_index(drop=True)
        required = {'productid', 'name', 'category', 'description', 'stock', 'season', 'price'}
        if not required.issubset(self.df.columns):
            raise ValueError('Catalog is missing required columns')
        if self.df.empty or self.df[list(required)].isna().any().any():
            raise ValueError('Catalog must contain complete product records')
        if self.df['productid'].duplicated().any():
            raise ValueError('Product IDs must be unique')
        self.df['price'] = pd.to_numeric(self.df['price'], errors='raise')
        import math
        if not self.df['price'].map(lambda x: math.isfinite(x) and x >= 0).all():
            raise ValueError('Prices must be finite and nonnegative')
        self.model_name = model_name
        self.model = None
        self.index = None
        self.documents = [self._document(row) for _, row in self.df.iterrows()]

    @staticmethod
    def _document(row):
        return '\n'.join(f'{label}: {row[key]}' for label, key in [
            ('Product ID', 'productid'), ('Name', 'name'), ('Category', 'category'),
            ('Description', 'description'), ('Stock', 'stock'), ('Season', 'season')
        ]) + f"\nPrice: ${row['price']}"

    def _ensure_index(self):
        if self.index is not None:
            return
        import faiss
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(self.model_name)
        embeddings = model.encode(self.documents, normalize_embeddings=True).astype('float32')
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        self.model, self.index = model, index

    def search(self, query, top_k=5, category=None, min_score=0.25):
        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
            raise ValueError('top_k must be a positive integer')
        if not -1 <= min_score <= 1:
            raise ValueError('min_score must be between -1 and 1')
        self._ensure_index()
        embedding = self.model.encode([query], normalize_embeddings=True).astype('float32')
        scores, indices = self.index.search(embedding, len(self.documents))
        results = []
        for score, index in zip(scores[0], indices[0]):
            if index < 0 or score < min_score:
                continue
            row = self.df.iloc[index]
            if category and str(row['category']).casefold() != category.casefold():
                continue
            result = self._row_to_result(row)
            result['score'] = float(score)
            results.append(result)
            if len(results) == top_k:
                break
        return results

    def _filtered(self, category):
        return self.df if category is None else self.df[
            self.df['category'].astype(str).str.casefold() == category.casefold()]

    def filter_by_category(self, category):
        if category is None:
            return []
        return [self._row_to_result(row) for _, row in self._filtered(category).iterrows()]

    def get_cheapest(self, category=None):
        df = self._filtered(category)
        return [] if df.empty else [self._row_to_result(df.loc[df['price'].idxmin()])]

    def get_most_expensive(self, category=None):
        df = self._filtered(category)
        return [] if df.empty else [self._row_to_result(df.loc[df['price'].idxmax()])]

    def _row_to_result(self, row):
        return {'document': self.documents[row.name], 'score': None,
                'product_id': str(row['productid'])}
