# Update the title of the book

>>> from bookshelf.models import Book
>>> book = Book.objects.get()
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> book.title
# 'Nineteen Eighty-Four'
