from datetime import date, datetime
from typing import Any, Dict, Union, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from authentication.models import CustomUser
from .models.comment import Comment
from .models.like import Like
from .models.post import Post
from .models.postReport import PostReport


class StatisticsView(LoginRequiredMixin, View):
    """ moderation panel with statistics """

    def get(self, request: Any) -> HttpResponse:
        if not request.user.is_superuser:
            raise PermissionDenied

        def cumulate_by_date(data: QuerySet, att: str = "created_at") -> dict[str, list[int] | list[Any]]:
            """ cumulate object by creation date """
            sorted(data, key=lambda x: getattr(x, att))
            labels = []
            counts = []

            c = 0
            for d in data:
                print(d)
                if len(labels) != 0 and labels[-1] != getattr(d, att).strftime("%Y-%m-%d"):
                    labels.append(getattr(d, att).strftime("%Y-%m-%d"))
                    counts.append(c)
                    c = 0
                c += 1

            if len(data) != 0:
                labels.append(getattr(d, att).strftime("%Y-%m-%d"))
                counts.append(c)

            return {'labels': labels, 'data': counts}

        nb_posts = Post.objects.all().count()
        nb_users = CustomUser.objects.all().count()
        nb_comments = Comment.objects.all().count()
        nb_reports = PostReport.objects.all().count()
        nb_likes = Like.objects.all().count()

        post_stat = cumulate_by_date(Post.objects.all())
        user_stat = cumulate_by_date(CustomUser.objects.all(), att="date_joined")

        context = {
            'nb_posts': nb_posts,
            'nb_users': nb_users,
            'nb_comments': nb_comments,
            'nb_reports': nb_reports,
            'nb_likes': nb_likes,

            'post_stat': post_stat,
            'user_stat': user_stat,
        }

        return render(request, 'blog/pages/statistics.html', context)
