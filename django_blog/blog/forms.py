from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django import forms
from .models import Post, Tag, Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Write your comment..."}
        ),
        label="",
        max_length=2000,
    )

    class Meta:
        model = Comment
        fields = ["content"]



# Extend UserCreationForm to add email
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]





class PostForm(forms.ModelForm):
       class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Write your post..."}
            ),
        }
    
    # A simple text input for tags (comma-separated). We'll parse this in the view.
        tags_input = forms.CharField(
            required=False,
            help_text="Enter tags separated by commas. Example: django, python, tips",
            widget=forms.TextInput(attrs={"placeholder": "tag1, tag2, tag3"}),
        )

        class Meta:
            model = Post
            fields = ["title", "content", "tags_input"]

        def __init__(self, *args, **kwargs):
            # if updating a post, pre-fill tags_input
            instance = kwargs.get("instance")
            super().__init__(*args, **kwargs)
            if instance:
                self.fields["tags_input"].initial = ", ".join(
                    [t.name for t in instance.tags.all()]
                )
