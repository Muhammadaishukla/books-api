# Books API

## Overview

This is a simple RESTful API for managing a collection of books. It allows users to perform CRUD (Create, Read, Update, Delete) operations on books. The API is built using FastAPI and uses an SQLite in-memory database for storage.

## Features

- Retrieve a list of all books
- Retrieve a specific book by its ID
- Create a new book
- Update an existing book by its ID
- Delete a book by its ID

## Requirements

- Docker
- Python 3.9 or higher

## Project Structure

```
/books_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── tests/
│       └── test_api.py
│
├── Dockerfile
├── readme.md
└── requirements.txt
```

## Setup

### Development

1. Clone the repository:

```bash
git clone https://github.com/Muhammadaishukla/books-api.git
cd books-api
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at `http://127.0.0.1:8001`.

### Docker

1. Build the Docker image:

```bash
docker build -t books_api .
```

2. Run the Docker container:

```bash
docker run -p 80:80 books_api
```

The API will be available at `http://localhost`.

## Testing

To run the tests, execute the following command:

```bash
pytest
```

## API Endpoints

| Method | Endpoint         | Description                      |
|--------|------------------|----------------------------------|
| GET    | `/books`         | Retrieve a list of all books.    |
| GET    | `/books/{id}`    | Retrieve a book by its ID.       |
| POST   | `/books`         | Create a new book.               |
| PUT    | `/books/{id}`    | Update an existing book by its ID. |
| DELETE | `/books/{id}`    | Delete a book by its ID.         |

## Models

### Book

- `id`: Integer, unique identifier for the book.
- `title`: String, title of the book.
- `author`: String, author of the book.
- `publication_year`: Integer, year the book was published.
