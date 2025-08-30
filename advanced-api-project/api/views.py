from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# --------------------------
# CRUD Views for Book Model
# --------------------------


class BookListView(generics.ListAPIView):
    """
    GET /books/
    Lists all books in the database.
    - Accessible to everyone (unauthenticated users can read).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # read-only, open


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<id>/
    Retrieves a single book by its ID.
    - Accessible to everyone.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Allows authenticated users to create a new book.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /books/<id>/update/
    Allows authenticated users to update an existing book.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<id>/delete/
    Allows authenticated users to delete a book.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
