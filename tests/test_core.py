import pytest
from src.query_router import QueryRouter
from src.retriever import ProductRetriever
from src.rag_pipeline import RAGPipeline

@pytest.mark.parametrize('query,intent,category', [
    ('Which is the cheapest laptop?', 'cheapest', 'Laptop'),
    ('most expensive gaming laptop', 'most_expensive', 'Gaming Laptop'),
    ('Show me smartphones', 'category_listing', 'Smartphone'),
    ('I need a laptop for programming', 'semantic_search', 'Laptop'),
    ('a realistic camera', 'semantic_search', 'Camera'),
    ('What is a catalyst?', 'semantic_search', None),
    ('List mice', 'category_listing', 'Mouse'),
    ('Show me something for travelling', 'semantic_search', None),
])
def test_router(query,intent,category):
    result=QueryRouter().analyze(query)
    assert result['intent']==intent
    assert result['filters'].get('category')==category

def test_exact_queries_use_real_catalog_without_models():
    retriever=ProductRetriever()
    pipeline=RAGPipeline(retriever=retriever)
    result=pipeline.run('cheapest laptop')
    assert result['results'][0]['product_id']=='P005'
    assert '$699' in result['answer']
    assert pipeline.run('most expensive laptop')['results'][0]['product_id']=='P001'
    assert {r['product_id'] for r in pipeline.run('show me smartphones')['results']}=={'P006','P007','P008'}
    assert retriever.index is None and pipeline.generator is None

def test_unknown_category_and_invalid_top_k():
    retriever=ProductRetriever()
    assert retriever.get_cheapest('Spaceship')==[]
    with pytest.raises(ValueError): retriever.search('laptop',top_k=0)

def test_empty_catalog_rejected(tmp_path):
    path=tmp_path/'empty.csv'
    path.write_text('productid,name,category,description,stock,season,price\n')
    with pytest.raises(ValueError): ProductRetriever(path)

class NoMatch:
    def search(self,*args,**kwargs): return []

class ForbiddenGenerator:
    def generate(self,*args): raise AssertionError('Must not generate without evidence')

def test_abstains_without_evidence():
    result=RAGPipeline(NoMatch(),ForbiddenGenerator()).run('Explain quantum gravity')
    assert result['results']==[]
    assert "enough information" in result['answer']

def test_context_passed_to_generator():
    class Retriever:
        def search(self,*args,**kwargs):
            return [{'document':'Name: Test laptop', 'product_id':'T001','score':0.9}]
    class Generator:
        def generate(self,query,context):
            assert query=='recommend a laptop'
            assert context=='Name: Test laptop'
            return 'Test laptop'
    assert RAGPipeline(Retriever(),Generator()).run('recommend a laptop')['answer']=='Test laptop'
