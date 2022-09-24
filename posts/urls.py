from .views import post_comment_create_and_list_view, like_unlike_post, PostDelete, PostUpdate
from django.urls import path

app_name = "posts"

urlpatterns = [
    path("", post_comment_create_and_list_view, name="main-post-view"),
    path("liked/", like_unlike_post, name="like-post-view"),
    path("<int:pk>/delete/", PostDelete.as_view(), name="post-delete-view"),
    path("<int:pk>/update/", PostUpdate.as_view(), name="post-update-view"),
]
