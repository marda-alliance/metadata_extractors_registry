# MaRDA WG Extractors Registry

A place to develop and discuss the MaRDA Extractors WG registry.

## Usage

Clone repository with submodules and install deps in a fresh Python virtualenv:

```
git clone git@github.com:marda-alliance/marda_extractors_registry --recurse-submodules
pip install -r requirements.txt
```

Use `invoke` and the tasks in `tasks.py` to generate pydantic models for all
schemas defined in the schema repo:

```
invoke regenerate-models
```

From the repository root directory, launch the server with uvicorn:

```
uvicorn src.marda_registry.app:app
```

then navigate to http://localhost:5000 to test.
