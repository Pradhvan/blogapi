from django.db import models
from django.contrib.postgres.search import SearchVectorField, SearchVector

from django.db import models
from django.contrib.postgres.indexes import GinIndex


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)

    # Add a SearchVectorField for full-text search
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["author"]),
            models.Index(fields=["created_at"]),
            # GIN index on the search_vector field
            GinIndex(fields=["search_vector"]),  # Use GinIndex for GIN indexing
        ]

    def update_search_vector(self):
        """
        This method updates the search_vector field for the Post model,
        combining the title and content fields.
        """
        self.search_vector = SearchVector("title", "content")

    def save(self, *args, **kwargs):
        # Update the search_vector before saving
        self.update_search_vector()
        super().save(*args, **kwargs)