from django.contrib import admin

from .models import User, Title


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


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
