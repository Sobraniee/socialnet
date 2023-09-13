from django.contrib import admin
from .models import *

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'likes', 'creator', 'status']
    list_filter = ['status', 'creator']
    search_fields = ['name', 'description', 'status', 'creator__username', 'creator__firstname']
    list_editable = ['status']
    inlines = [CommentInline]

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Short)
admin.site.register(SavedPosts)
admin.site.register(Notification)