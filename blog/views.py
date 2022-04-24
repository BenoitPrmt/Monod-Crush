import logging

from auth.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import *
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views.generic.edit import DeletionMixin

from .models import Post, Comment, Like

log = logging.getLogger(__name__)


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    paginate_by = 30

    def get_queryset(self) -> QuerySet[Post]:
        posts = Post.objects.filter(status__in=Post.PUBLIC).order_by('-created_at')
        if self.request.user.is_authenticated:
            for post in posts:
                post.liked = post.likes.filter(user=self.request.user).exists()
        return posts


# comment view login required for post but  not for get
class CommentView(View):
    """ login required for post"""

    def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponse('login required', status=401)

        post = get_object_or_404(Post, id=post_id)
        comment = request.POST['comment']

        Comment.objects.create(post=post, author=request.user, text=comment, is_anonymous=True)

        comments = post.comments.order_by('-created_at')
        return render(request, 'blog/partials/rep.html', {'comments': comments, 'post': post})

    def get(self, request: HttpRequest, post_id: int) -> HttpResponse:
        post = Post.objects.get(id=post_id)
        post.comments.order_by('-created_at')

        comments = post.comments.order_by('-created_at')
        return render(request, 'blog/partials/rep.html', {'comments': comments, 'post': post})


# class PartialPostCommentDetail(DetailView):
#     model = Post
#     template_name = 'blog/partial_post_comment.html'
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comments'] = self.object.comment_set.all()
#         return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['text', "is_anonymous"]
    template_name = 'blog/create_post.html'
    success_url = '/'

    def form_valid(self, form) -> HttpResponseRedirect:
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['text']


class PostView(LoginRequiredMixin, DeletionMixin, View):
    model = Post


class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self, queryset=None) -> CustomUser:
        return get_object_or_404(CustomUser, username=self.kwargs['username'])


class UserEditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'first_name', 'bio', "study", 'email', 'instagram', 'twitter', 'github', 'website']
    template_name = 'blog/edit_profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self, queryset=None) -> CustomUser:
        return get_object_or_404(CustomUser, username=self.kwargs['username'])

    def get_success_url(self) -> HttpResponseRedirect:
        """ Redirect to new user profile page if user is editing his own username """
        return reverse('blog:user-profile', kwargs={'username': self.object.username})


class UserDeleteProfileView(LoginRequiredMixin, DeletionMixin, View):
    model = CustomUser
    slug_url_kwarg = 'username'
    slug_field = 'username'
    success_url = reverse_lazy('blog:index')

    # def get_object(self, queryset=None) -> CustomUser:
    #     return get_object_or_404(CustomUser, username=self.kwargs['username'])


class SearchView(ListView):
    model = CustomUser
    template_name = "blog/search_results.html"
    context_object_name = "users"

    def get_queryset(self) -> QuerySet[CustomUser]:
        query = self.request.GET.get("q", "")
        user_list = CustomUser.objects.filter(
                Q(username__icontains=query) | Q(first_name__icontains=query)
        )
        return user_list


class LikeView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
        post = get_object_or_404(Post, id=post_id)

        if not post.likes.filter(user=request.user).exists():
            Like.objects.create(user=request.user, post=post)
            log.info(f"User {request.user} liked post {post}")
            post.liked = True

            return render(request, 'blog/components/post-like-button.html', {'post': post})
        else:
            post.likes.filter(user=request.user.id).delete()
            log.info(f"User {request.user} unliked post {post}")

            post.liked = False
            return render(request, 'blog/components/post-like-button.html', {'post': post})
