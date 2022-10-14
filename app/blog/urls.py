from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import BlogView, CommentPerPostListView, ListCreateUserCommentView, EditUserCommentView, TagView, ListCreateReplyView, EditReplyView

router = DefaultRouter()
router.register('blog', BlogView, basename='blog')
router.register('tags', TagView, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('blog/<slug:slug>/comments/', CommentPerPostListView.as_view(), name='blog-comments'),      # list all the comments on a post
    path('blog/<slug:slug>/comment/', ListCreateUserCommentView.as_view(), name='new-comment'),  # list and create new comment by a user on a single post
    path('blog/<slug:slug>/comment/edit/<int:pk>/', EditUserCommentView.as_view(), name='comment-detail'), # update or delete comment
    path('blog/<slug:slug>/comment/<int:comment_id>/reply/', ListCreateReplyView.as_view(), name='new-reply'),
    path('blog/<slug:slug>/comment/<int:comment_id>/reply/edit/<int:pk>/', EditReplyView.as_view(), name='reply-detail'),
    ]
