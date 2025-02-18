import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("silk/", include("silk.urls", namespace="silk")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
