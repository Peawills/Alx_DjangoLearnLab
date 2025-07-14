>>> from bookshelf.models import Book
>>> book = Book.objects.first()
>>> book.title
# '1984'
>>> book.author
# 'George Orwell'
>>> book.publication_year
# 1949