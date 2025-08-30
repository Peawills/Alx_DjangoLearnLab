from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)
from . import views

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),  # /  -> list
    path(
        "posts/", PostListView.as_view(), name="post-list"
    ),  # /posts/ (optional duplicate route)
    path("posts/new/", PostCreateView.as_view(), name="post-create"),  # create
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),  # detail
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="blog/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="blog/logout.html"),
        name="logout",
    ),
]
