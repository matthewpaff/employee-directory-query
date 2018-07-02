"""Original generated examples with independent expected results."""

def make_case(index):
    ident = 10 * (index + 1)
    a = {"id": ident, "tenant": "north", "name": "Employee_" + str(index), "department": "engineering"}
    b = {"id": ident + 1, "tenant": "north", "name": "Colleague_" + str(index), "department": "support"}
    foreign = {"id": ident, "tenant": "south", "name": "Other tenant", "department": "engineering"}
    def item(row):
        return {key: row[key] for key in ("id", "name", "department")}
    data = {"tenant": "north", "employees": [b, foreign, a], "limit": 1}
    kind = index % 8
    description = "page tenant records in ascending employee order"
    expected = {"items": [item(a)], "next_cursor": ident}
    if kind == 1:
        data["department"] = "support"
        expected = {"items": [item(b)], "next_cursor": None}
        description = "filter tenant records by department"
    elif kind == 2:
        data["after_id"] = ident
        expected = {"items": [item(b)], "next_cursor": None}
        description = "continue paging after the supplied employee cursor"
    elif kind == 3:
        data["employees"] = [foreign]
        expected = {"items": [], "next_cursor": None}
        description = "exclude records from another tenant"
    elif kind == 4:
        data["limit"] = True
        description = "reject boolean page limits"
    elif kind == 5:
        data["employees"] = [a, a.copy()]
        description = "reject duplicate employee IDs within a tenant"
    elif kind == 6:
        del data["tenant"]
        description = "require an explicit tenant selection"
    elif kind == 7:
        data["employees"] = []
        expected = {"items": [], "next_cursor": None}
        description = "return an empty page for an empty directory"
    case = {"id": "directory-{:04d}".format(index), "description": description, "input": data}
    case.update({"expected_error": True} if kind in (4, 5, 6) else {"expected": expected})
    return case
