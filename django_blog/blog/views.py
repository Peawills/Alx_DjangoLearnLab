from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CommentForm



# --- Post views (PostCreateView/PostUpdateView should set tags using tags_input) ---


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # Save post without tags first so we have an instance
        form.instance.author = self.request.user
        response = super().form_valid(form)
        tags_input = form.cleaned_data.get("tags_input", "")
        assign_tags_to_post(self.object, tags_input)
        messages.success(self.request, "Post created.")
        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        tags_input = form.cleaned_data.get("tags_input", "")
        assign_tags_to_post(self.object, tags_input)
        messages.success(self.request, "Post updated.")
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# assign_tags_to_post helper
def assign_tags_to_post(post, tags_input):
    """
    tags_input: comma-separated string of tag names
    Ensures tag objects exist and assigns them to the post.
    """
    # Normalize and split
    names = [t.strip() for t in tags_input.split(",") if t.strip()]
    # Find or create Tag objects
    tags = []
    for name in names:
        tag, _ = Tag.objects.get_or_create(name__iexact=False, defaults={"name": name})
        # get_or_create with case-insensitive is clunky; instead try get then create
        if not tag:
            try:
                tag = Tag.objects.get(name__iexact=name)
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name=name)
        tags.append(tag)
    # assign
    post.tags.set(tags)


# --- Tag list (posts by tag) ---
class PostsByTagListView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        self.tag = get_object_or_404(Tag, slug=slug)
        return self.tag.posts.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag"] = self.tag
        return ctx


# --- Search view ---
class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if not query:
            return Post.objects.none()
        # search title, content, and tag name
        return Post.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        # ensure post exists
        self.post = get_object_or_404(Post, pk=kwargs.get("post_id"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        # after creating a comment, go back to the post detail page
        return reverse("post-detail", kwargs={"pk": self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # default would be blog/post_list.html
    context_object_name = "posts"
    paginate_by = 10  # optional


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()  # blank form for inline comment
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        # Only the author can edit
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        # Only the author can delete
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)


# Registration view
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            messages.success(request, "Your account has been created!")
            return redirect("profile")
    else:
        form = UserRegisterForm()
    return render(request, "blog/register.html", {"form": form})


# Profile view
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, "blog/profile.html", {"u_form": u_form})
