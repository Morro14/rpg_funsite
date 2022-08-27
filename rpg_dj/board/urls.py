from django.urls import path
from .views import NewPostView, PostsList, NewsList, NewsArticle, post_view, CommentDelete, PostUpdate, PostDelete, \
    PostDetail, comment_accept, comment_save
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', PostsList.as_view()),
    path('new-post/', NewPostView.as_view(), name='new_post'),
    path('posts/', PostsList.as_view(), name='posts'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),


    path('news/', NewsList.as_view(), name='news'),
    path('news-article/<int:pk>', NewsArticle.as_view(), name='news_article'),

    path('<str:user>/comments', post_view, name='post_personal'),
    path('comments/<int:pk>/delete', CommentDelete.as_view(), name='comment_delete'),
    path('<str:user>/comments/<int:pk>', comment_accept, name='comment_accept'),
    path('post/<int:pk>/comment-accept', comment_save, name='comment_accept'),

]
