from .models import Author, Library

# Query all books by a specific author
books_by_author = Author.objects.get(name="John Doe").books.all()

# List all books in a library
library_books = Library.objects.get(name="Central Library").books.all()

# Retrieve the librarian for a library
librarian = Library.objects.get(name="Central Library").librarian
