def test_request_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_request_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data


def test_request_404(client):
    response = client.get("/error")
    assert response.status_code == 404
    # Check that the 404 page actually loads on the front end
    assert b"Oops!" in response.data


def test_request_navbar(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/">Welcome'
    assert b'href="/about"' in response.data

