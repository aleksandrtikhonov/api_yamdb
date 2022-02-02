from django.contrib import admin

from .models import User, Title, Category, Genre, Genre_Title, Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name'
    )
    list_editable = ('role',)
    search_fields = ('username', 'email')
    list_filter = ('role',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name',
        'year', 'category_id',
    )
    list_editable = ('category_id',)
    list_filter = ('year', 'category_id')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'score',
        'pub_date',
    )
    list_editable = ('text', 'author', 'score',)
    search_fields = ('author', 'score',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review_id',
        'text',
        'author',
        'pub_date',
    )
    list_editable = ('text', 'author',)
    search_fields = ('review_id', 'author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Genre_Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
