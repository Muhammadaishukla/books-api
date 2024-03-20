from sqlmodel import SQLModel, create_engine, Field
from typing import Optional

class BookBase(SQLModel):
    title: str
    author: str
    publication_year: int

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int = Field(default=None, primary_key=True)

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publication_year: Optional[int] = None

class Book(BookBase, table=True):
    id: int = Field(default=None, primary_key=True)

# SQLite in-memory database; it will be cleared on every restart
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})