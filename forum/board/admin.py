from django.contrib import admin
from .models import Board, Category, Topic, Post


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    model = Board
    readonly_fields = ('slug', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ('slug', )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    model = Topic
    readonly_fields = ('slug', )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
