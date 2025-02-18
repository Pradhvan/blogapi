# Demo API

- Simple blog API built to play with django-filters and PostgreSQL Native Full-Text Search, built to close [1039](https://github.com/carltongibson/django-filter/issues/1039)

- Also uses Django Debug Toolbar and Silk for basic profiling of ORM queries while using Full-Text Search.

- Implements a custom [CountlessPaginator](https://github.com/Pradhvan/blogapi/blob/main/api/paginators.py#L49) to bypass the costly COUNT(*) query, which Django’s default paginator uses to determine the number of pages. This came in handy as I was generating 1,00,000+ posts in the database with the [management command](https://github.com/Pradhvan/blogapi/blob/main/api/management/commands/populate_posts.py).
