from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet
from rest_framework.authtoken.views import obtain_auth_token  # ✅ Token view

router = DefaultRouter()
router.register(r"books_all", BookViewSet, basename="book_all")

urlpatterns = [
    path("books/", BookList.as_view(), name="book-list"),
    path("token/", obtain_auth_token, name="api-token"),  # ✅ Token endpoint
    path("", include(router.urls)),
]
