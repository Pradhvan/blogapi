from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from .filters import PostFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .paginators import CountlessPaginator

class PostListCreate(generics.ListAPIView):
    queryset = Post.objects.select_related("author").order_by('created_at')
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_paginated_response(self, data):
        page_number = self.request.GET.get("page")
        paginator = CountlessPaginator(self.queryset, 10)
        page_obj = paginator.get_page(page_number)

        return Response({
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'results': data
        })


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related("author").order_by("created_at")
    serializer_class = PostSerializer