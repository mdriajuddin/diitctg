from django.urls import path

from .views import PostListCreateView, PostDetailView

urlpatterns = [


    # Blog endpoints
    path('api/v1/posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('api/v1/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
