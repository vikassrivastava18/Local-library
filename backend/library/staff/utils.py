import json
import os
import random

from django.conf import settings

from catalog.models import Author


def load_books_data(genre_name: str) -> dict:
    file_path = os.path.join(
        settings.BASE_DIR,
        "catalog/books_data",
        f"{genre_name}.json"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError("Book data file not found")

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def generate_isbn13() -> str:
    digits = [random.randint(0, 9) for _ in range(12)]
    checksum = sum(d * 3 if i % 2 else d for i, d in enumerate(digits))
    digits.append((10 - checksum % 10) % 10)
    return "".join(map(str, digits))


def get_author(author_name: str):
    parts = author_name.strip().split()
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ""

    author, _ = Author.objects.get_or_create(
        first_name=first,
        last_name=last
    )
    return author


def extract_book_info(book: dict) -> dict:
    info = book.get("volumeInfo", {})

    author_name = (info.get("authors") or ["Unknown"])[0]
    author = get_author(author_name)

    identifiers = info.get("industryIdentifiers", [])
    isbn = identifiers[0]["identifier"] if identifiers else generate_isbn13()

    return {
        "author": author,
        "title": info.get("title", ""),
        "summary": info.get("description", ""),
        "isbn": isbn,
        "cover_url": info.get("imageLinks", {}).get("thumbnail", "")
    }




