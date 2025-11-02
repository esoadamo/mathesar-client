# Mathesar Python Client

A typed, ergonomic Python client for the Mathesar JSON-RPC API.

- Transport: JSON-RPC over HTTP
- Auth: Basic auth (username/password)
- Python: 3.13+
- Dependencies: pydantic v2, requests

## Quick start

```python
from mathesar_client import MathesarClient

# Configure base URL and credentials via env or initialize the raw client accordingly
client = MathesarClient()  # uses defaults from MathesarClientRaw()

# Work with a database
db = client.database(database_id=1)

# Schemas
schemas = db.list_schemas()
public = db.schema_by_name("public")

# Tables
users = public.table_by_name("users")

# Records: returns column names and inlines linked summaries
page = users.records_list(limit=10, order_by=[("id", "asc")])
for row in page.results:
    print(row)

# Add a record using column names
new_row = users.record_add({
    "email": "jane@example.com",
    "full_name": "Jane Doe",
})

# Columns: create a UUID primary key
users.add_primary_key_column(pkey_type="UUIDv4", name="id")

# Constraints: add a unique constraint on email
users.add_unique_constraint(columns=["email"], name="uq_users_email")

# Data modeling: suggest types for a table
suggested = users.suggest_types()
print(suggested)
```

## Package layout

- `mathesar_client.client_raw_models`: Pydantic models for all API entities
- `mathesar_client.client_raw`: Low-level raw client mapping API methods 1:1
- `mathesar_client.client`: High-level client with `Database → Schema → Table` hierarchy and QoL

## Notes

- The high-level client resolves column names↔attnums automatically where relevant.
- Record lists are enriched with column names and inline linked summaries when requested.
- For foreign keys, referent table column identifiers are passed as-is; if you prefer names, resolve them with that table's column cache.
