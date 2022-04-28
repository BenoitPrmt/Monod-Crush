from django.urls import path

from .views import PostCreateView, PostEditView, PostListView, PostDeleteView, PostCommentView, PostLikeView, \
    ProfileView, ProfileEditView, ProfileDeleteView, ProfilSearchView, \
    ProfileStarView, PostReportView, PostHideView, ModerationView


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),

    path('post/new', PostCreateView.as_view(), name='new-post'),
    path('post/<int:post_id>/edit', PostEditView.as_view(), name='edit-post'),
    path('post/<int:post_id>/delete', PostDeleteView.as_view(), name='delete-post'),
    path('post/<int:post_id>/comment', PostCommentView.as_view(), name='comment-post'),
    path('post/<int:post_id>/like', PostLikeView.as_view(), name='like-post'),
    path('post/<int:post_id>/report', PostReportView.as_view(), name='report-post'),
    path('post/<int:post_id>/hide', PostHideView.as_view(), name='hide-post'),

    path('user/<str:username>', ProfileView.as_view(), name='profile'),
    path('user/<str:username>/edit', ProfileEditView.as_view(), name='edit-profile'),
    path('user/<str:username>/delete', ProfileDeleteView.as_view(), name='delete-profile'),
    path('user/<str:username>/star', ProfileStarView.as_view(), name='start-profile'),
    path("search", ProfilSearchView.as_view(), name="search"),

    path('comment/<int:comment_id>/delete', PostCommentView.as_view(), name='delete-comment'),
    path('comment/<int:comment_id>/like', PostLikeView.as_view(), name='like-comment'),
    path('comment/<int:comment_id>/report', PostReportView.as_view(), name='report-comment'),
    path('comment/<int:comment_id>/hide', PostHideView.as_view(), name='hide-comment'),

    path('moderation', ModerationView.as_view(), name='moderation'),

]
