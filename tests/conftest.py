import pytest
import os
import tempfile
from flaskr.db import *
from flaskr import create_app


print(__file__)

with open(os.path.join(os.path.dirname(__file__), "data.sql"), 'rb') as f:
    sql_script = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        "TESTING": True,
        "DATABASE": db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(sql_script)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
