from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("category/<slug:slug>/", views.CategoryListView.as_view(), name="category_detail"),
    path("tag/<slug:slug>/", views.TagListView.as_view(), name="tag_detail"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<slug:slug>/comment/", views.post_comment, name="post_comment"),
]
