# REST API

Start: `python -m uvicorn src.api:app --host 127.0.0.1 --port 8000`

| Endpoint | Behavior |
|---|---|
| `GET /health` | Liveness and catalog-initialization state; does not verify model readiness |
| `POST /query` | Query the catalog |
| `GET /docs` | Interactive OpenAPI documentation |

Request: `{"query":"cheapest laptop"}`. The query must be a string of 1–1,000 characters after whitespace trimming. Extra fields are rejected.

The response contains `query`, `intent`, `filters`, `results`, and `answer`. Each result includes `product_id`, `document`, and `score` (null for exact retrieval).

- `200`: completed, including insufficient-information responses.
- `422`: invalid request fields.
- `503`: inference busy, initialization failure, or model/inference error. Busy responses include `Retry-After: 5`.

The API serializes requests that reach inference. It does not queue them. A single worker is the documented configuration. Initialization is lazy; a health response alone does not mean models are downloaded. The Streamlit interface uses the pipeline directly and does not use the API's inference lock.

Do not expose the demonstration server publicly without authentication, TLS, body-size limits, rate limits, and a resource budget. A request field limit is not an HTTP body-size limit. Server exceptions are logged without explicitly logging request bodies; use appropriate log handling in any deployment.
