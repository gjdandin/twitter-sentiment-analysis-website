import pytest
from flask import Flask
import json
from routes import configure_routes
import templates, os

def app_constructor():
    """Creates a mock test flask app to test with"""
    app = Flask(__name__, template_folder=r"C:\Users\gilha\Dropbox\tests-twitter-analyse\templates")
    app.debug = True
    configure_routes(app)
    app = app.test_client()
    return app


def test_index():
    """Test index page"""
    client = app_constructor()

    url = "/"
    response = client.get(url)
    assert response.status_code == 200
    assert "Insert a twitter hashtag or a topic:" in str(response.data)


def test_callback():
    """Test that callback route returns correct responses"""
    client = app_constructor()

    url = "/callback?searchterm=Oslo&numsearch=20"
    response = client.get(url)

    assert response.status_code == 200
    assert "Oslo" in str(response.data)
    assert "20" in str(response.data) #Assert that the search queries are in the response

    assert "piegraphJSON" in str(response.data) #Assert that the visualization jsons are in response
    assert "bargraphJSON" in str(response.data)  # Assert that the visualization jsons are in response

    assert "neutralsample" in str(response.data) # Assert that the samples are in the response
    assert "negativesample" in str(response.data)
    assert "positivesample" in str(response.data)


def test_callback_failure():
    """Test that a callback with missing queries returns an error"""
    client = app_constructor()
    url = "/callback?searchterm=&numsearch="

    response = client.get(url)

    assert response.status_code == 404 #Assert that it sends an error
    assert "Norway" not in str(response.data) #Make sure that default values are not returned as well
    assert "10" not in str(response.data)
    assert "piegraphJSON" not in str(response.data)  # Assert that the visualization jsons are not in response
    assert "bargraphJSON" not in str(response.data)