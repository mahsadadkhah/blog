from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'slug', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('updated',)
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)


admin.site.register(Comment)
