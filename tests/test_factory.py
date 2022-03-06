from flask.testing import FlaskClient

from flaskr import create_app


def test_config() -> None:
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_index_page(client: FlaskClient) -> None:
    """Test index page."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data is not None
