from django.contrib import admin
from .models import Category, Tag, Post, PostImage, Comment

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at", "is_featured")
    list_filter = ("status", "is_featured", "category")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PostImageInline]
    raw_id_fields = ("author",)
    date_hierarchy = "published_at"
    filter_horizontal = ("tags",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "author", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("body", "name", "email")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
