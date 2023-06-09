from django import forms
from .models import Post


class PostUpdateCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)

