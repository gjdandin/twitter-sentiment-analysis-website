import pytest
from flask import Flask
import json
from routes import configure_routes
import os


# Build a constructor for testapp


def test_index():
    app = Flask(__name__, template_folder=r"C:\Users\Gilhan Jentrix\Dropbox\tests-twitter-analyse\templates")
    app.debug = True
    configure_routes(app)
    client = app.test_client()
    url = "/"
    response = client.get(url)
    assert "Insert a twitter hashtag or a topic:" in str(response.data)


def test_callback():
    app = Flask(__name__)
    app.debug = True
    configure_routes(app)
    client = app.test_client()
    url = "/callback?searchterm=Oslo&numsearch=20"

    response = client.get(url)
    assert response.status_code == 200
