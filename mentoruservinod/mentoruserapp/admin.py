from django.contrib import admin
from .models import CustomUser, Conversation
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active','is_mentor')
    list_filter = ('email', 'is_staff', 'is_active','is_mentor')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_mentor')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register your models here.


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Conversation)