from django.contrib import admin
from .models import (
    User,
    Author
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'email']
    date_hierarchy = 'created_at'
    readonly_fields = ['password', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'password')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email', 'follower_count', 'post_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__name', 'user__email', 'website']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user']
    readonly_fields = ['follower_count', 'post_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Link', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('avatar', 'website', 'social_links')
        }),
        ('Statistics', {
            'fields': ('follower_count', 'post_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
