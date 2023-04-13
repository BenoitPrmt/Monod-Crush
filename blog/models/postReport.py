import logging
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from authentication.models import CustomUser
from blog.models.post import Post

log = logging.getLogger(__name__)


class PostReport(models.Model):
    # threshold beyond which the publication is hidden
    REPORTS_CRITICAL_THRESHOLD = 3

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports", verbose_name="post signalé")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports",
                             verbose_name="auteur du signalement")
    created_at = models.DateTimeField("date du signalement", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_report_post_user'),
        ]

        verbose_name = "signalement"
        verbose_name_plural = "signalements"

        permissions = (
            # user permission
            ("report_posts", "Peut signaler des posts"),

            # moderator permission
            ("reset_reports", "Peut réinitialiser les signalements d'un post"),
        )

        default_permissions = ()

    def validate_unique(self, exclude: Any = None) -> None:
        """ Check you can't report the same post twice """
        if PostReport.objects.filter(post=self.post, user=self.user).exists():
            raise ValidationError("The post has already been reported by this user.", code='unique_report_post_user')
        super().validate_unique(exclude)

    def clean(self) -> None:
        """ Check you can't report your own post """
        if self.post.author == self.user:
            raise ValidationError("The post author can't report his own post.", code='author_post')

    def save(self, **kwargs) -> None:
        """ Override save method to prevent more than 3 reports per post """
        super().save(**kwargs)

        self.post.status = Post.PostStatus.AWAITING_VERIFICATION

        if self.post.nb_of_reports >= self.REPORTS_CRITICAL_THRESHOLD:
            self.post.status = Post.PostStatus.HIDDEN
            log.info(f"Post {self.post.id} has been hidden (reported {self.post.nb_of_reports} times.)")

        self.post.save()

    def __repr__(self) -> str:
        return f'{self.post} - {self.user.username}'
