from django.urls import path
from . import views
from .views import (AddPostView, UpdatePostView, PostDetailView, DeletePostView,
                    PostLikeToggle, PostLikeAPIToggle, PostListView,
                    CategoryPostListView, UserPostListView)

urlpatterns = [
    path('post-image/', AddPostView.as_view(), name='add_post'),
    path('post/detail/<int:pk>', PostDetailView.as_view(), name='detail_post'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name="per-category"),
    path('post/like/<int:pk>/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/like/<int:pk>/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('gallery/', PostListView.as_view(), name='gallery'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.autocompleteModel, name='search_auto'),
]