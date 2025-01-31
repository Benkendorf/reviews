from django.contrib import admin

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year',
                    'description', 'category', 'genres')
    list_editable = ('category',)
    search_fields = ('name', 'genre', 'category', 'year')
    filter_horizontal = ('genre',)

    @admin.display
    def genres(self, obj):
        return ', '.join([g.name for g in list(obj.genre.all())])


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')


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
    list_display = ('id', 'review', 'text', 'author', 'pub_date')
    search_fields = ('title', 'text')
