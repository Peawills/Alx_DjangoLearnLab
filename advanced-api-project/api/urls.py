from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),  # GET all
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),  # GET one
    path("books/create/", BookCreateView.as_view(), name="book-create"),  # POST
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="book-update"),  # PUT
    path(
        "books/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete"
    ),  # DELETE
]
