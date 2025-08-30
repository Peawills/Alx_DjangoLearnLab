from rest_framework import serializers
from .models import Author, Book
from django.utils.timezone import now


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model:
    - Serializes all book fields
    - Includes custom validation to ensure publication_year is not in the future
    """

    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value):
        """
        Ensure the book's publication year is not greater than the current year.
        """
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model:
    - Includes author's name
    - Nested serializer for all related books
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
