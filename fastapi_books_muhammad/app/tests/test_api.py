import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from app.main import app, get_session


# Create a new engine instance for testing
@pytest.fixture(name="test_db", scope="module")
def fixture_test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client", scope="module")
def fixture_client(test_db):
    def get_test_db_override():
        with Session(test_db) as session:
            yield session

    # Set the dependency override for the test client
    app.dependency_overrides[get_session] = get_test_db_override
    with TestClient(app) as testing_client:
        yield testing_client
    # Clear the dependency override after the tests are done
    app.dependency_overrides.clear()

def test_create_book(client):
    book_data = {"title": "Test Book", "author": "Author Name", "publication_year": 2021}
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["publication_year"] == book_data["publication_year"]
    assert "id" in data

def test_read_book(client):
    book_data = {"title": "Test Book", "author": "Author Name", "publication_year": 2021}
    response = client.post("/books/", json=book_data)
    book_id = response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["publication_year"] == book_data["publication_year"]

def test_update_book(client):
    book_data = {"title": "Old Book", "author": "Author Name", "publication_year": 2020}
    response = client.post("/books/", json=book_data)
    book_id = response.json()["id"]

    update_data = {"title": "Updated Book", "author": "New Author", "publication_year": 2022}
    response = client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == update_data["title"]
    assert data["author"] == update_data["author"]
    assert data["publication_year"] == update_data["publication_year"]

def test_delete_book(client):
    book_data = {"title": "Book to Delete", "author": "Author to Delete", "publication_year": 2021}
    response = client.post("/books/", json=book_data)
    book_id = response.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404

def test_list_books(client):
    for i in range(3):
        book_data = {"title": f"Book {i}", "author": f"Author {i}", "publication_year": 2021 + i}
        client.post("/books/", json=book_data)

    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
