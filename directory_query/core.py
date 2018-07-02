"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value

def query_employees(data):
    fields(data, ("tenant", "employees"), ("department", "after_id", "limit"))
    tenant = label(data["tenant"])
    department = label(data["department"]) if "department" in data else None
    after = integer(data.get("after_id", 0))
    limit = integer(data.get("limit", 20), 1, 50)
    found, seen = [], set()
    for row in sequence(data["employees"], 1000):
        fields(row, ("id", "tenant", "name", "department"))
        ident, row_tenant = integer(row["id"], 1), label(row["tenant"])
        name, dept = label(row["name"]), label(row["department"])
        key = (row_tenant, ident)
        if key in seen:
            raise ValueError("Duplicate tenant/employee ID")
        seen.add(key)
        if row_tenant == tenant and ident > after and (department is None or dept == department):
            found.append({"id": ident, "name": name, "department": dept})
    found.sort(key=lambda row: row["id"])
    page = found[:limit]
    return {"items": page, "next_cursor": page[-1]["id"] if len(found) > limit else None}
