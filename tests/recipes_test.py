from app.db.models import Recipe
from flask import session
import pytest


def test_browse_recipes(client):
    assert client.post("/login", data={"email": "admin2@mail.com", "password": "Test123!"}).headers[
               'Location'] == "/recipes/mine"
    assert client.get("/recipes").status_code == 200


def test_browse_admin_recipes(client):
    assert client.post("/login", data={"email": "admin@mail.com", "password": "Test123!"}).headers[
               'Location'] == "/recipes/mine"
    assert client.get("/recipes/admin").status_code == 200


def test_add_recipe(client):
    with client:
        assert client.post("/login", data={"email": "admin2@mail.com", "password": "Test123!"}).headers[
                   'Location'] == "/recipes/mine"
        assert client.get("/recipes/add").status_code == 200
        response = client.post("/recipes/add", data={"recipe_title": "Pytest Recipe",
                                                     "recipe_content": "Automatically generated test recipe"})
        assert response.headers['Location'] == "/recipes/mine"
        with client.application.app_context():
            assert Recipe.query.filter_by(title="Pytest Recipe").first().get_id() is not None


def test_edit_recipe(client):
    with client:
        assert client.post("/login", data={"email": "admin2@mail.com", "password": "Test123!"}).headers[
                   'Location'] == "/recipes/mine"
        with client.application.app_context():
            recipe_id = Recipe.query.filter_by(title="Pytest Recipe").first().get_id()
            recipe_url = "/recipes/edit/" + str(recipe_id)
        assert client.get(recipe_url).status_code == 200
        response = client.post(recipe_url, data={"recipe_title": "New Pytest",
                                                 "recipe_content": "Automatically generated test recipe"})
        assert response.headers['Location'] == "/recipes/mine"
        with client.application.app_context():
            recipe_id = Recipe.query.filter_by(title="New Pytest").first().get_id()
            assert Recipe.query.filter_by(id=recipe_id).first().get_title() == "New Pytest"


def test_delete_recipe(client):
    with client:
        assert client.post("/login", data={"email": "admin2@mail.com", "password": "Test123!"}).headers[
                   'Location'] == "/recipes/mine"
        with client.application.app_context():
            recipe_id = Recipe.query.filter_by(title="New Pytest").first().get_id()
            recipe_url = "/recipes/delete/" + str(recipe_id)
        assert client.post(recipe_url).status_code == 302
        with client.application.app_context():
            assert Recipe.query.filter_by(id=recipe_id).first() is None


def test_deny_delete_access(client):
    with client:
        assert client.post("/login", data={"email": "admin2@mail.com", "password": "Test123!"}).headers[
                   'Location'] == "/recipes/mine"
        with client.application.app_context():
            recipe_id = Recipe.query.filter_by(user_id=1).first().get_id()
            recipe_url = "/recipes/delete/" + str(recipe_id)
        assert client.post(recipe_url).status_code == 302
        with client.application.app_context():
            assert Recipe.query.filter_by(id=recipe_id).first() is not None
