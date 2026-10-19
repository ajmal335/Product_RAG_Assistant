"""Offline routing/exact-retrieval regression evaluation, not LLM benchmarking."""
import json
from pathlib import Path
from src.rag_pipeline import RAGPipeline

CASES = [
    ('cheapest laptop', 'cheapest', ['P005']),
    ('most expensive laptop', 'most_expensive', ['P001']),
    ('lowest price smartphone', 'cheapest', ['P008']),
    ('highest price smartphone', 'most_expensive', ['P006']),
    ('show me headphones', 'category_listing', ['P009', 'P010']),
    ('list gaming laptops', 'category_listing', ['P004']),
    ('cheapest mouse', 'cheapest', ['P013']),
    ('show me tablets', 'category_listing', ['P017']),
]

def main():
    pipeline = RAGPipeline()
    rows = []
    for query, intent, ids in CASES:
        result = pipeline.run(query)
        actual = [r['product_id'] for r in result['results']]
        rows.append({'query': query, 'expected_ids': ids, 'actual_ids': actual,
                     'passed': result['intent'] == intent and actual == ids})
    report = {'scope': '8 hand-selected exact/routing regression cases; no neural inference',
              'passed': sum(r['passed'] for r in rows), 'total': len(rows), 'cases': rows}
    path = Path(__file__).resolve().parents[1] / 'results' / 'structured_evaluation.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] == report['total'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
