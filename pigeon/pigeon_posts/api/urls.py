from django.urls import path

from pigeon_posts.api.views import PostDetailView, PostListView, PostDeleteView

app_name = "pigeon_posts"

urlpatterns = [
    path('', PostListView.as_view()),
    path('post/<pk>/', PostDetailView.as_view()),
    path('post/<pk>/delete/', PostDeleteView.as_view()),
]
