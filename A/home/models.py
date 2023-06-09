from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=500)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.title} - {self.author} - {self.updated}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - `{self.body[:30]}'

