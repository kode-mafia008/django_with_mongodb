from django.contrib import admin
from .models import (
    Category,
    Tag,
    Draft,
    Post,
    PostVersion,
    PostStatistics,
    Comment,
    Bookmark,
    Notification,
    PostSchedule
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'created_at']
    list_filter = ['created_at', 'parent']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['color']


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'scheduled_publish_at', 'created_at']
    list_filter = ['status', 'created_at', 'scheduled_publish_at']
    search_fields = ['title', 'content', 'author__user__name']
    date_hierarchy = 'created_at'
    raw_id_fields = ['author']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content', 'author__user__name']
    date_hierarchy = 'created_at'
    raw_id_fields = ['author']


@admin.register(PostVersion)
class PostVersionAdmin(admin.ModelAdmin):
    list_display = ['post', 'version_number', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'title', 'content']
    date_hierarchy = 'created_at'
    raw_id_fields = ['post', 'created_by']
    readonly_fields = ['version_number']


@admin.register(PostStatistics)
class PostStatisticsAdmin(admin.ModelAdmin):
    list_display = ['post', 'view_count', 'like_count', 'share_count', 'last_viewed_at']
    list_filter = ['last_viewed_at']
    search_fields = ['post__title']
    raw_id_fields = ['post']
    readonly_fields = ['view_count', 'like_count', 'share_count', 'avg_read_time', 'last_viewed_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content_preview', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['content', 'post__title', 'author__user__name']
    date_hierarchy = 'created_at'
    raw_id_fields = ['post', 'author', 'parent']
    list_editable = ['is_approved']
    actions = ['approve_comments', 'unapprove_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'
    
    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_comments.short_description = 'Unapprove selected comments'


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__user__name', 'post__title', 'notes']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user', 'post']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'message_preview', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__user__name', 'message']
    date_hierarchy = 'created_at'
    raw_id_fields = ['recipient']
    list_editable = ['is_read']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = 'Mark selected as unread'


@admin.register(PostSchedule)
class PostScheduleAdmin(admin.ModelAdmin):
    list_display = ['post', 'scheduled_for', 'published_at', 'is_published', 'retry_count']
    list_filter = ['is_published', 'scheduled_for', 'published_at']
    search_fields = ['post__title']
    date_hierarchy = 'scheduled_for'
    raw_id_fields = ['post']
    list_editable = ['is_published']
    readonly_fields = ['retry_count']
