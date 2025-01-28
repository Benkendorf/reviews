from django.contrib import admin

# Register your models here.
from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year',
                    'description', 'category', 'rating')
    search_fields = ('name', 'genre', 'category', 'year')
    filter_horizontal = ('genre',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', 'text', 'score')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'review', 'text', 'author', 'pub_date')
    search_fields = ('title', 'text', 'score')
