from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client = APIClient()
        self.client.login(username="testuser", password="testpass123")

        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            published_year=2024,
        )

        self.book_list_url = reverse("book-list")  # from DRF router
        self.book_detail_url = reverse("book-detail", args=[self.book.id])

    def test_get_books_list(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "published_year": 2025,
        }
        response = self.client.post(self.book_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest("id").title, "New Book")

    def test_retrieve_single_book(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "published_year": 2026,
        }
        response = self.client.put(self.book_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_unauthenticated_access(self):
        client = APIClient()  # fresh client without login
        response = client.get(self.book_list_url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # or 401 depending on your settings

    def test_filter_books(self):
        response = self.client.get(self.book_list_url, {"author": "Author Name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(book["author"] == "Author Name" for book in response.data))

    def test_search_books(self):
        response = self.client.get(self.book_list_url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Test" in book["title"] for book in response.data))

    def test_order_books(self):
        response = self.client.get(self.book_list_url, {"ordering": "-published_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
