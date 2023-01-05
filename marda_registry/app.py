#!/usr/bin/env python

from pydantic import BaseModel
from uuid import UUID
from fastapi import FastAPI
import mongomock as pymongo
import uvicorn
import pathlib 
import json
from functools import lru_cache

from typing import Type

from .models import FileType


class Extractor(BaseModel):
    authors: list[str] | None
    uuid: UUID
    contact: list[str]
    input_file_types: list[UUID]


app = FastAPI()

db = pymongo.MongoClient().registry


@app.get("/filetypes")
def get_filetypes():
    return list(db.filetypes.find())

@app.get("/filetypes/{uuid}", response_model=FileType)
def get_filetype(uuid: str):
    return list(db.filetypes.find({"uuid": uuid}))

@app.get("/search-filetypes")
def search_file_types(query: str):
    return db.filetypes.find({"$text": query})

@app.get("/extractors")
def get_extractors():
    return list(db.extractors.find({}))

@app.get("/extractors/{uuid}", response_model=Extractor)
def get_extractor(uuid: str):
    return list(db.extractors.find({"uuid": uuid}))

@app.get("/search-extractors")
def search_file_types(query: str):
    return db.extractors.find({"$text": query})

@app.get("/")
def get_info():
    return _get_info()


@lru_cache(maxsize=1)
def _get_info():
    with open(pathlib.Path(__file__).parent / "registry" / "meta.json") as f:
        meta = json.load(f)
    return meta

@app.on_event("startup")
async def load_data():

    def load_registry_collection(model: Type, validate: bool = False):
        name = model.__name__.lower() + "s"
        data_file = pathlib.Path(__file__).parent / "registry" / f"{name}.json"
        with open(data_file, "r") as f:
            data = json.load(f)
        assert isinstance(data[name], list)

        if validate:
            for entry in data[name]:
                model(**entry)

        db[name].insert_many(data[name])

    load_registry_collection(Extractor)
    load_registry_collection(FileType)

    _get_info()


if __name__ == "__main__":
    uvicorn.run("__main__:app")
