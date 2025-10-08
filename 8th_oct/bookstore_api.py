from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model
class Books(BaseModel):
    id : int
    title: str
    author : str
    price : float
    in_stock : bool


# in-memory database
books = [
    {"id": 1, "title": "ABC murders", "author": "Agatha Cristie", "price": 450.00, "in_stock" : True },
    {"id": 2, "title": "The hound of baskerville", "author": "Arthur Conan Doyle", "price": 500.00 , "in_stock" : False},
    {"id": 3, "title": "Dracula", "author": "Bram Stoker", "price": 750.00, "in_stock" : True }
]

# GET all request
@app.get("/books")
def get_all():
    return {"Books": books}

# Count of Total books
@app.get("/books/count", status_code=200)
def count_books():
    count = len(books)
    if count > 0:
        return {"Total number of books ": count}
    else:
        # Status code 404 is used when the list is empty
        raise HTTPException(status_code=404, detail="No Book found")


# POST a record
@app.post("/books", status_code=201)
def add_book(book: Books):
    present_ids = []
    for record in books:
        present_ids.append(record["id"])
    if book.dict()["id"] not in present_ids:
        books.append(book.dict())
        return {"message": "Book added successfully", "Book": books}
    else:
        raise HTTPException(status_code=404, detail="Book already exists")


# PUT request
@app.put("/books/{book_id}")
def update_books(book_id: int, updated_book: Books):
    for i, record in enumerate(books):
        if record["id"] == book_id:
            books[i] = updated_book.dict()
            return {"message": "Book updated successfully", "Book": books[i]}
    raise HTTPException(status_code=404, detail="book not found")


# DELETE Request
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, s in enumerate(books):
        if s["id"] == book_id:
            books.pop(i)
            return {"message": "Book Deleted Successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


# Books by author and Price

@app.get("/books/search")
def search_books(author_name: str):
   for i,record in enumerate(books):
       if record["author"] == author_name:
           return books[i]
   raise HTTPException(status_code=404, detail="Book not found")


def search_books_under_500():
    results = []
    for book in books:
        if book["price"] < 500:
            results.append(results)

        else:
            raise HTTPException(status_code=404, detail="No book found under this 500")

        return results
    return None