import django_filters
from django_filters import Filter
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from .models import Post

class FullTextSearchFilter(Filter):
    def __init__(self, fields=None, *args, **kwargs):
        """
        - `fields`: List of model fields to include in full-text search.
        """
        self.fields = fields or []
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value or not self.fields:
            return qs  # Return original queryset if no search term is provided

        # Build a SearchVector dynamically from specified fields
        search_vector = SearchVector(*self.fields)

        # Apply full-text search query
        search_query = SearchQuery(value)

        return qs.annotate(search=search_vector).filter(search=search_query)


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")  # Regular title filter
    created_at = django_filters.DateFromToRangeFilter()  # Date filter
    updated_at = django_filters.DateFromToRangeFilter()  # Date filter

    # Full-text search filter using a custom method
    # search = django_filters.CharFilter(field_name="content", method="search_fulltext")
    search = FullTextSearchFilter(fields=["content"])  
    author_name = django_filters.CharFilter(
        field_name="author__name", lookup_expr="icontains"
    )

    class Meta:
        model = Post
        fields = ["title", "created_at", "updated_at", "author_name"]

    # def search_fulltext(self, queryset, field_name, value):
    #     """
    #     Optimized full-text search using indexed search vectors.
    #     """
    #     return queryset.filter(search_vector=SearchQuery(value)).annotate(
    #         rank=SearchRank('search_vector', SearchQuery(value))
    #     ).filter(rank__gt=0).order_by('-rank')

    def search_fulltext(self, queryset, name, value):
        """
        Optimized full-text search using indexed search vectors.
        """
        search_query = SearchQuery(value)  # Create a SearchQuery object from the value
        return queryset.filter(search_vector=search_query).annotate(
            search_rank=SearchRank('search_vector', search_query)  # Renamed to avoid conflict
        ).filter(search_rank__gt=0).order_by('-search_rank')
