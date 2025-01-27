from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('<int:pk>/post-like', views.AddPostLikeView.as_view(), name='post_like'),
    path('<int:pk>/comment-form/', views.PostDetailView.as_view(), name='post_comment_form'),
    path('<int:pk>/comment-reply-form/', views.CommentDetailView.as_view(), name='comment_reply_form'),
    path('<int:pk>/comment/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('<int:pk>/comment-like/', views.AddCommentLike.as_view(), name='comment_like'),
    path('<int:pk>/comment-dislike/', views.AddCommentDislike.as_view(), name='comment_dislike'),
    path('<int:pk>/replies/', views.CommentRepliesView.as_view(), name='comment_replies'),
    path('<int:pk>/reply/', views.CommentReplyDetailView.as_view(), name='reply_detail'),
    # path('<int:pk>/reply-form/', views.CommentReplyDetailView.as_view(), name='reply_form'),
    path('<int:pk>/reply-like/', views.AddReplyLike.as_view(), name='reply_like'),
    path('<int:pk>/reply-dislike/', views.AddReplyDislike.as_view(), name='reply_dislike'),
    path('<slug:slug>/comments/', views.PostCommentsView.as_view(), name='post_comments'),
    path('<slug:category_slug>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/', views.CategoryPostsView.as_view(), name='category_detail'),
    # path('<slug:slug>/', views.PostCommentsView.as_view(), name='post_comments'),
]
