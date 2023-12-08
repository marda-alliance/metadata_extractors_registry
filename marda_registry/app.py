#!/usr/bin/env python

import json
import pathlib
from functools import lru_cache

import mongomock as pymongo
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .models import Extractor, FileType
from .utils import load_registry_collection

__api_version__ = "0.3.0"


app = FastAPI(
    title="MaRDA extractors registry API",
    description=f"This server implements v{__api_version__} of the [MaRDA extractors WG](https://github.com/marda-alliance/metadata_extractors) registry API.",  # noqa: E501
    version=__api_version__,
)

api = FastAPI()

db: pymongo.Database = pymongo.MongoClient().registry

templates = Jinja2Templates(directory=pathlib.Path(__file__).parent / "templates")

app.mount(
    "/static",
    StaticFiles(directory=pathlib.Path(__file__).parent / "static"),
    name="static",
)


class JSONAPIResponse(BaseModel):
    data: list[FileType] | list[Extractor] | FileType | Extractor
    meta: dict | None = None


class FileTypeEntryResponse(JSONAPIResponse):
    data: list[FileType]


class ExtractorEntryResponse(JSONAPIResponse):
    data: list[Extractor]


class SingleFileTypeEntryResponse(JSONAPIResponse):
    data: FileType


class SingleExtractorEntryResponse(JSONAPIResponse):
    data: Extractor


@api.get("/filetypes", response_model=FileTypeEntryResponse)
def get_filetypes():
    return {"data": list(db.filetypes.find(projection={"_id": 0})), "meta": _get_info()}


@app.get("/filetypes", response_class=HTMLResponse)
def get_filetypes_html(request: Request):
    return templates.TemplateResponse(
        "filetypes.html", {"request": request, "data": get_filetypes()["data"]}
    )


@api.get("/filetypes/{id}", response_model=SingleFileTypeEntryResponse)
def get_filetype(id: str):
    result = db.filetypes.find_one({"id": id.lower()}, projection={"_id": 0})

    registered_extractors = db.extractors.find(
        {"supported_filetypes.id": id}, projection={"id": 1}
    )
    if not result:
        raise HTTPException(status_code=404, detail="File type not found")

    result["registered_extractors"] = {_["id"] for _ in registered_extractors}
    return {"data": result, "meta": _get_info()}


@app.get("/filetypes/{id}", response_class=HTMLResponse)
def get_filetype_html(request: Request, id: str):
    try:
        ft = get_filetype(id)["data"]
    except HTTPException:
        ft = None
    return templates.TemplateResponse("filetype.html", {"request": request, "ft": ft})


@api.get("/search-filetypes", response_model=FileTypeEntryResponse)
def search_file_types(query: str):
    results = list(db.filetypes.find({"$text": query}, projection={"_id": 0}))
    return {"data": results, "meta": _get_info()}


@api.get("/extractors", response_model=ExtractorEntryResponse)
def get_extractors():
    return {
        "data": list(db.extractors.find({}, projection={"_id": 0})),
        "meta": _get_info(),
    }


@app.get("/extractors")
def get_extractors_html(request: Request):
    return templates.TemplateResponse(
        "extractors.html", {"request": request, "data": get_extractors()["data"]}
    )


@api.get("/extractors/{id}", response_model=SingleExtractorEntryResponse)
def get_extractor(id: str):
    result = db.extractors.find_one({"id": id.lower()}, projection={"_id": 0})
    if not result:
        raise HTTPException(status_code=404, detail="File type not found")
    return {"data": result, "meta": _get_info()}


@app.get("/extractors/{id}")
def get_extractor_html(request: Request, id: str):
    try:
        ex = get_extractor(id)["data"]
    except HTTPException:
        ex = None
    return templates.TemplateResponse("extractor.html", {"request": request, "ex": ex})


@api.get("/search-extractors", response_model=ExtractorEntryResponse)
def search_extractors(query: str):
    results = list(db.extractors.find({"$text": query}, projection={"_id": 0}))
    return {"data": results, "meta": _get_info()}


@api.get("/")
def get_info():
    return _get_info()


@app.get("/", response_class=HTMLResponse)
def get_index_html(request: Request):
    """Simply return the file types list as the "homepage" for now."""
    return get_filetypes_html(request)


@lru_cache(maxsize=1)
def _get_info():
    with open(pathlib.Path(__file__).parent / "data" / "meta.json") as f:
        meta = json.load(f)
    meta["api_version"] = __api_version__
    return meta


@app.on_event("startup")
async def load_data():
    load_registry_collection(Extractor, database=db)
    load_registry_collection(FileType, database=db)

    _get_info()


app.mount(f"/api/v{__api_version__}", api)
app.mount("/api/", api)


if __name__ == "__main__":
    uvicorn.run("__main__:app")
