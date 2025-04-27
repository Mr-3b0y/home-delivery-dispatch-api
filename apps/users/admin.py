from django.contrib import admin

# Register your models here.


from apps.users.models.user_model import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin view for the User model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)