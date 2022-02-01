from django.contrib import admin

from .models import User, Title, Category, Genre, Genre_Title


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
        'year', 'category',
    )
    list_editable = ('category',)
    list_filter = ('year', 'category')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Genre_Title)
