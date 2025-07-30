from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    path("register/", views.register_view, name="register"),
    path("admin-role/", views.admin_view, name="admin_view"),
    path("librarian-role/", views.librarian_view, name="librarian_view"),
    path("member-role/", views.member_view, name="member_view"),
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/edit/<int:pk>/", views.edit_book, name="edit_book"),
    path("books/delete/<int:pk>/", views.delete_book, name="delete_book"),
]
