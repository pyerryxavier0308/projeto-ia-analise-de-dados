import pytest
from fastapi.testclient import TestClient
from app_core.api import app
from app_core.ml import get_model

@pytest.fixture(scope='session')
def client(tmp_path_factory):
    import os
    root = tmp_path_factory.mktemp('projeto_ia')
    old_db = os.environ.get('PROJECT_DB_PATH')
    old_model = os.environ.get('PROJECT_MODEL_PATH')
    os.environ['PROJECT_DB_PATH']=str(root/'test.sqlite3')
    os.environ['PROJECT_MODEL_PATH']=str(root/'test_model.joblib')
    get_model.cache_clear()
    try:
        with TestClient(app) as c:
            yield c
    finally:
        if old_db is None:os.environ.pop('PROJECT_DB_PATH',None)
        else:os.environ['PROJECT_DB_PATH']=old_db
        if old_model is None:os.environ.pop('PROJECT_MODEL_PATH',None)
        else:os.environ['PROJECT_MODEL_PATH']=old_model
        get_model.cache_clear()
