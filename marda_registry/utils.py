import glob
import pathlib
from typing import Type

import mongomock as pymongo
import yaml


def load_registry_collection(
    model: Type, database: pymongo.Database | None = None, validate: bool = True
) -> int:
    """Loads any entries of the specified model ty pes from the corresponding data directory,
    optionally validating and inserting them into the given database.

    Parameters:
        model: The type to load.
        database: The database to insert the entries into.
        validate: Whether to validate the entries before inserting them into the database.

    Returns:
        The number of entries ingested for that type.

    """
    name = model.__name__.lower() + "s"
    entries = glob.glob(str(pathlib.Path(__file__).parent / "data" / name / "*.yml"))
    for entry in entries:
        with open(entry, "r") as f:
            data = yaml.safe_load(f)
        if validate:
            model(**data)
        if database:
            database[name].insert_one(data)

    return len(entries)
