"""Local REST interface. Serialize inference to protect shared model resources."""
import logging
from threading import Lock
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

logger = logging.getLogger(__name__)
app = FastAPI(title='Product RAG Assistant', version='1.1.0')
_pipeline = None
_init_lock = Lock()
_inference_lock = Lock()

class QueryRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    query: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1000)]

class RetrievedProduct(BaseModel):
    product_id: str
    document: str
    score: float | None

class QueryResponse(BaseModel):
    query: str
    intent: str
    filters: dict[str, str]
    results: list[RetrievedProduct]
    answer: str

def get_pipeline():
    global _pipeline
    with _init_lock:
        if _pipeline is None:
            try:
                from src.rag_pipeline import RAGPipeline
                _pipeline = RAGPipeline()
            except Exception:
                logger.exception('Catalog initialization failed')
                raise HTTPException(503, 'Catalog unavailable') from None
    return _pipeline

@app.get('/health')
def health():
    return {'status': 'ok', 'catalog_initialized': _pipeline is not None,
            'note': 'Liveness only; model downloads and inference are not checked.'}

@app.post('/query', response_model=QueryResponse)
def query(payload: QueryRequest, pipeline=Depends(get_pipeline)):
    if not _inference_lock.acquire(blocking=False):
        raise HTTPException(503, 'Inference busy; retry later', headers={'Retry-After': '5'})
    try:
        return pipeline.run(payload.query)
    except Exception:
        logger.exception('Inference failed')
        raise HTTPException(503, 'Inference unavailable; check server logs') from None
    finally:
        _inference_lock.release()
