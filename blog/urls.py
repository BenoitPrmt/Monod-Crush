from django.urls import path

from .views import PostCreateView, PostEditView, PostView, PostListView, CommentView, UserProfileView, SearchView, \
    UserEditProfileView, UserDeleteProfileView, LikeView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),

    path('post/new', PostCreateView.as_view(), name='post-new'),
    path('post/<int:post_id>/edit', PostEditView.as_view(), name='post-edit'),
    path('post/<int:post_id>/', PostView.as_view(), name='post'),

    path('post/<int:post_id>/comment', CommentView.as_view(), name='post-comment'),
    path('post/<int:post_id>/like', LikeView.as_view(), name='like-post'),

    path('user/<str:username>', UserProfileView.as_view(), name='user-profile'),
    path('user/<str:username>/edit', UserEditProfileView.as_view(), name='edit-profile'),
    path('user/<str:username>/delete', UserDeleteProfileView.as_view(), name='delete-profile'),

    path("search", SearchView.as_view(), name="search"),
]
