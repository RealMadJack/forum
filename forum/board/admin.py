from django.contrib import admin
from .models import Board, Category, Topic, Post


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    model = Board
    readonly_fields = ('slug', )
    list_display = (
        'name', 'created', 'modified',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ('slug', )
    list_display = (
        'name', 'board', 'created', 'modified',
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    model = Topic
    readonly_fields = ('slug', )
    list_display = (
        'name', 'short_message', 'category', 'user', 'created', 'modified',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = (
        'user', 'short_message', 'topic', 'created', 'modified',
    )
