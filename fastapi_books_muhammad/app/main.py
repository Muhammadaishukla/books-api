from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select, SQLModel

from .models import Book, BookCreate, BookRead, engine

SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/books")
async def read_books(session: Session = Depends(get_session)):
    result = session.exec(select(Book)).all()
    return result

@app.get("/books/{book_id}")
async def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookRead, status_code=201)
async def create_book(book_create: BookCreate, session: Session = Depends(get_session)):
    book = Book.from_orm(book_create)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.put("/books/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book_update: BookCreate, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book_update.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(book, key, value)
    session.commit()
    session.refresh(book)
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": "Book deleted successfully"}