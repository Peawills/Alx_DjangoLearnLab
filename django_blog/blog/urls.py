from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    register,
    profile,
)

urlpatterns = [
    path(
        "post/<int:post_id>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-edit"),
    path(
        "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
    # Blog post URLs
    path("", PostListView.as_view(), name="post-list"),  # Home / list of posts
    path(
        "post/<int:pk>/", PostDetailView.as_view(), name="post-detail"
    ),  # View one post
    path("post/new/", PostCreateView.as_view(), name="post-create"),  # Create a post
    path(
        "post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"
    ),  # Update a post
    path(
        "post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"
    ),  # Delete a post
    # User authentication URLs
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
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
    # Password reset URLs (optional but good to have)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="blog/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="blog/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="blog/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="blog/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
