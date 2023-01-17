#!/usr/bin/env python

import json
import pathlib
from functools import lru_cache
from typing import List, Type

import mongomock as pymongo
import uvicorn
from fastapi import FastAPI, HTTPException

from .models import Extractor, FileType

__api_version__ = "0.1.0"


app = FastAPI(
    title="MaRDA extractors registry API",
    description=f"This server implements v{__api_version__} of the [MaRDA extractors WG](https://github.com/marda-alliance/metadata_extractors) registry API.",  # noqa: E501
    version=__api_version__,
)

db = pymongo.MongoClient().registry


@app.get("/filetypes")
def get_filetypes():
    return list(db.filetypes.find())


@app.get("/filetypes/{id}", response_model=FileType)
def get_filetype(id: str):
    result = db.filetypes.find_one({"id": id.lower()}, projection={"_id": 0})
    if not result:
        raise HTTPException(status_code=404, detail="File type not found")
    return result


@app.get("/search-filetypes", response_model=List[FileType])
def search_file_types(query: str):
    results = list(db.filetypes.find({"$text": query}, projection={"_id": 0}))
    return results


@app.get("/extractors")
def get_extractors():
    return list(db.extractors.find({}, projection={"_id": 0}))


@app.get("/extractors/{id}", response_model=Extractor)
def get_extractor(id: str):
    result = db.extractors.find_one({"id": id.lower()}, projection={"_id": 0})
    if not result:
        raise HTTPException(status_code=404, detail="File type not found")
    return result


@app.get("/search-extractors", response_model=List[Extractor])
def search_extractors(query: str):
    results = list(db.extractors.find({"$text": query}, projection={"_id": 0}))
    return results


@app.get("/")
def get_info():
    return _get_info()


@lru_cache(maxsize=1)
def _get_info():
    with open(pathlib.Path(__file__).parent / "data" / "meta.json") as f:
        meta = json.load(f)
    meta["api_version"] = __api_version__
    return meta


@app.on_event("startup")
async def load_data():
    def load_registry_collection(model: Type, validate: bool = True):
        name = model.__name__.lower() + "s"
        data_file = pathlib.Path(__file__).parent / "data" / f"{name}.json"
        with open(data_file, "r") as f:
            data = json.load(f)
        assert isinstance(data[name], list)

        if validate:
            for entry in data[name]:
                model(**entry)

        if data[name]:
            db[name].insert_many(data[name])

    load_registry_collection(Extractor)
    load_registry_collection(FileType)

    _get_info()


if __name__ == "__main__":
    uvicorn.run("__main__:app")
