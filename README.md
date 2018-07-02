# Employee Directory Query

Filter supplied synthetic employee records by tenant and department with cursor pagination.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external server, Redis, Celery, or network access is required.

## Run

```console
python -m directory_query --help
python -m directory_query examples/sample.json
python -m directory_query --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Requires tenant and employees; accepts department, after_id (default 0), and limit (1–50, default 20). Up to 1000 employee objects contain positive id, tenant, name, and department. Tenant/id pairs must be unique. Results contain only the requested tenant and sort by ID; next_cursor is present only if more matching rows remain. This is supplied-data filtering, not authentication, a database, or a production tenant-isolation boundary.

## Learning focus

The modeled 2018 tenant-aware directory and backend API learning themes. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `directory_query/core.py`: validated parsing, storage, or state transitions.
- `directory_query/cli.py`: JSON command interface.
- `directory_query/generate_fixtures.py`: original deterministic validation cases.
- `directory_query/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 544 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
