from django.contrib import admin

from .models import Announcement, Category, Notice


@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Announcement) 
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at', 'expires_at', 'moderation_status', 'display_status')
    list_filter = ('moderation_status', 'category', 'published_at', 'expires_at')
    search_fields = ('title', 'content', 'author__username')
    autocomplete_fields = ('category', 'author')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'expires_at', 'status')
    list_filter = ('expires_at', 'created_at')
    search_fields = ('title', 'content')
