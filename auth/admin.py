from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = CustomUserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'first_name', 'is_active', 'is_staff')
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ('username', "email", "first_name")
    ordering = ('username',)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('username', 'profile_pic')}),
        ("Informations personnelles", {'fields': ('first_name', 'email', 'date_of_birth',)}),
        ("Réseaux sociaux", {'fields': ('instagram', 'twitter', 'website')}),
        ("Permissions", {'fields': ('is_staff', 'is_active')}),
        ("Permissions avancées", {'fields': ('is_superuser', 'groups', 'user_permissions'),
                                  'classes': ('collapse',)}),
        ("Dates", {"fields": ("last_login", "date_joined"),
                   'classes': ('collapse',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'date_of_birth', 'password1', 'password2'),
        }),
        ("Permissions", {'fields': ('is_superuser', 'groups', 'user_permissions'),
                         'classes': ('collapse',)}),
    )


# Now register the new UserAdmin...
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.login_template = 'auth/login.html'
