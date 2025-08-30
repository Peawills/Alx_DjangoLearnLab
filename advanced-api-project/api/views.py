
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions, filters
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer


# Everyone can view books, with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Add filtering, search, and ordering
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filtering by fields
    filterset_fields = ["title", "author", "publication_year"]

    # Searching (case-insensitive partial matches)
    search_fields = ["title", "author"]

    # Ordering (example: ?ordering=title or ?ordering=-publication_year)
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]  # default ordering


# Example: Only authenticated users can retrieve
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Example: Only authenticated users can create
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Example: Only staff can update
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]


# Example: Only staff can delete
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
