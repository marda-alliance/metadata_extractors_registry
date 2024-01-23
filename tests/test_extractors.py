from marda_extractors_api import extract
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from marda_registry.app import api
    yield TestClient(app=api)

LFS_PATH = Path(__file__).parent.parent / "marda_registry" / "data" / "lfs"

@pytest.mark.parametrize("ft_id", [d.name for d in LFS_PATH.glob("*")])
def test_files(ft_id, client):
    ft_files = (LFS_PATH / ft_id).glob("*")
    with client as cli:
        response = cli.get(f"/filetypes/{ft_id}")
        assert response.status_code == 200
        response = response.json()
        assert response 
        supported_extractors = response.get("supported_extractors")
        assert supported_extractors is not None
