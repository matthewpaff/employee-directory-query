import unittest
from pathlib import Path
from directory_query.core import query_employees as evaluate
from directory_query.fixture_check import check


class CoreTests(unittest.TestCase):

    def test_shared_ids_do_not_cross_tenants(self):
        rows = [{"id": 1, "tenant": "a", "name": "A", "department": "ops"}, {"id": 1, "tenant": "b", "name": "B", "department": "ops"}]
        self.assertEqual(evaluate({"tenant": "a", "employees": rows}), {"items": [{"id": 1, "name": "A", "department": "ops"}], "next_cursor": None})

    def test_cursor_after_last_match_is_empty(self):
        data = {"tenant": "a", "employees": [{"id": 2, "tenant": "a", "name": "A", "department": "ops"}], "after_id": 2}
        self.assertEqual(evaluate(data), {"items": [], "next_cursor": None})

    def test_page_limits_and_duplicate_records_are_validated(self):
        with self.assertRaises(ValueError):
            evaluate({"tenant": "a", "employees": [], "limit": 51})
        row = {"id": 1, "tenant": "a", "name": "A", "department": "ops"}
        with self.assertRaises(ValueError):
            evaluate({"tenant": "a", "employees": [row, row]})

    def test_complete_fixture_corpus(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", evaluate), 500)


if __name__ == "__main__":
    unittest.main()
