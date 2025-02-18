from django.contrib import admin
from api.models import Post, Author  # Import your Post model


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("created_at",)


admin.site.register(Author)
