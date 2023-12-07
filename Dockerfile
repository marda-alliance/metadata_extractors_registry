from python:3.11-slim-buster

env PORT=8000
workdir /app

# Copy local version of the registry and install reqs
copy requirements.txt /app
run pip install -r requirements.txt

copy schemas /app/schemas
copy marda_registry /app/marda_registry
copy tasks.py /app

# Regenerate models from the current schemas
run invoke regenerate-models

# Validate all entries against the schema
run invoke validate-entries

cmd uvicorn marda_registry.app:app --host 0.0.0.0 --port ${PORT}

healthcheck --interval=5m --timeout=3s --start-period=10s \
  cmd curl --fail http://localhost:${PORT}/api || exit 1
