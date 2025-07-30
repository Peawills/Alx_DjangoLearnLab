from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Library
from .models import Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from .forms import BookForm


@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("list_books")  # Replace with your actual list view name
    return render(request, "relationship_app/book_form.html", {"form": form})


@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect("list_books")  # Replace with your actual list view name
    return render(
        request, "relationship_app/book_form.html", {"form": form, "book": book}
    )


# Delete Book
@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "relationship_app/book_confirm_delete.html", {"book": book})


# View All Books
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, "relationship_app/book_list.html", {"books": books})


# Role check functions
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"


def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"


def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# Admin view
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


# Librarian view
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


# Member view
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # replace 'home' with the name of your landing view
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view to show a specific library's details and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
