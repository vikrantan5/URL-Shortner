from django.contrib import admin
from .models import UserProfile, UserLink

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'username', 'created_at']
    search_fields = ['display_name', 'username', 'user__username']

@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = ['profile', 'link_type', 'title', 'display_order', 'is_active']
    list_filter = ['link_type', 'is_active']
    search_fields = ['title', 'url']
