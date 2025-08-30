from django.db import models
from django.utils.timezone import now


class Author(models.Model):
    """
    Author model:
    Represents a book author with a one-to-many relationship to books.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model:
    Each book belongs to one Author (ForeignKey relationship).
    """

    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
