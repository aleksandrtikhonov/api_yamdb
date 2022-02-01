from django.contrib import admin

from .models import User


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


admin.site.register(User, UserAdmin)
