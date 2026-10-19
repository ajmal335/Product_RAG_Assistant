# Engineering walkthrough

## Decisions to understand

1. Exact minimum/maximum queries are computed from the catalog, because a language model need not perform arithmetic.
2. Model initialization is lazy. Exact queries and tests can run without downloading weights.
3. The pipeline accepts retriever/generator dependencies so tests can isolate orchestration from external models.
4. The API exposes source records alongside an answer so a caller can inspect evidence.
5. A nonblocking lock returns 503 for concurrent inference instead of allowing unbounded model work.

## October 2026 changes

Added the FastAPI interface, local Docker configuration, test suite, and structured evaluation. Fixed the router's `I need` misclassification and gaming-laptop category specificity. Added catalog validation and location-independent catalog loading. Replaced environment-specific package pins with portable version constraints; this is not a fully locked environment.

These engineering additions were developed with AI assistance. Review the code and reproduce the tests before presenting them as skills in an interview. Existing model experiments and reported metrics have not been rerun by this update.

## Practice questions

- Why do exact queries bypass FLAN-T5?
- When can a similarity threshold reject a useful answer?
- Why do unit tests with a fake generator not establish answer accuracy?
- What happens if two API requests arrive during model loading?
- What needs to change before public deployment?

## Verification commands

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m experiments.evaluate_structured
```

Full-model smoke test, after installing full requirements and allowing model downloads: call `/query` with `Which laptop is good for programming?`, inspect the retrieved documents and answer, and record the actual latency and quality. This smoke test remains to be run on a model-capable host.
