import pytest
from fastapi.testclient import TestClient
from src.api import app, get_pipeline, _inference_lock
from src.rag_pipeline import RAGPipeline

@pytest.fixture
def client():
    pipeline=RAGPipeline()
    app.dependency_overrides[get_pipeline]=lambda: pipeline
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_health_and_real_exact_query(client):
    assert client.get('/health').status_code==200
    response=client.post('/query',json={'query':' cheapest laptop '})
    assert response.status_code==200
    assert response.json()['results'][0]['product_id']=='P005'
    assert response.json()['query']=='cheapest laptop'

@pytest.mark.parametrize('payload',[{}, {'query':''}, {'query':'   '}, {'query':42},
    {'query':'x'*1001}, {'query':'hi','unknown':True}])
def test_invalid_payload(client,payload):
    assert client.post('/query',json=payload).status_code==422

def test_busy_returns_retry_header(client):
    _inference_lock.acquire()
    try:
        response=client.post('/query',json={'query':'cheapest laptop'})
        assert response.status_code==503
        assert response.headers['retry-after']=='5'
    finally: _inference_lock.release()

def test_failure_is_sanitized_and_lock_released(client):
    class Broken:
        def run(self,query): raise RuntimeError('private-path')
    app.dependency_overrides[get_pipeline]=lambda: Broken()
    response=client.post('/query',json={'query':'hello'})
    assert response.status_code==503
    assert 'private-path' not in response.text
    assert not _inference_lock.locked()
