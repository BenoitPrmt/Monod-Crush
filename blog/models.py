from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet

from auth.models import CustomUser


class Post(models.Model):
    NORMAl = 'N'
    HIDDEN = 'H'
    DELETED = 'D'

    PUBLIC = (
        NORMAl,
    )

    STATUS_CHOICES = (
        (NORMAl, 'Normal'),
        (HIDDEN, 'Masqué'),
        (DELETED, 'Supprimé'),
    )

    text = models.TextField(max_length=500)
    author: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                           related_name='posts', verbose_name='Auteur')
    created_at = models.DateTimeField("date de création", auto_now_add=True)
    updated_at = models.DateTimeField("dernière modification", auto_now=True)
    status = models.CharField("état", max_length=1, choices=STATUS_CHOICES, default=NORMAl)
    is_anonymous = models.BooleanField("post anonyme", default=True)

    likes: QuerySet["Like"]
    reports: QuerySet["Report"]
    comments: QuerySet["Comment"]

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

        permissions = (
            ('edit_other_users_posts', 'Can edit other users\' posts'),
            ('delete_other_users_posts', 'Can delete other users\' posts'),
            ('hide_unhide_posts', 'Can hide/unhide posts'),
            ('view_hidden_posts', 'Can view hidden posts'),
            ('show_author_name_when_anonymous', 'Can show author name when anonymous'),
        )

    @property
    def nb_of_likes(self) -> int:
        return self.likes.count()

    @property
    def nb_of_comments(self) -> int:
        return self.comments.count()

    @property
    def nb_of_reports(self) -> int:
        return self.reports.count()

    def is_liked_by(self, user: CustomUser) -> bool:
        """ Returns True if the user has liked the post. """
        return self.likes.filter(user=user).exists()

    def is_reported_by(self, user: CustomUser) -> bool:
        """ Returns True if the user has reported the post. """
        return self.reports.filter(user=user).exists()

    @property
    def short_text(self) -> str:
        """ Returns the first 40 characters of the post's text. """
        MAX_LENGTH = 40
        if len(self.text) > MAX_LENGTH:
            return self.text[:MAX_LENGTH] + '...'
        else:
            return self.text

    def __str__(self) -> str:
        return f"{self.author.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class Comment(models.Model):
    post: Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="post")
    author: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                           related_name="comments", verbose_name='auteur')
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField("date de creation", auto_now_add=True)
    is_anonymous = models.BooleanField("commentaire anonyme", default=True)

    class Meta:
        verbose_name = "commentaire"
        verbose_name_plural = "commentaires"

        permissions = (
            ('delete_other_users_comments', 'Can delete other users\' comments'),
            ('edit_other_users_comments', 'Can edit other users\' comments'),
            ('hide_unhide_comments', 'Can hide/unhide comments'),
            ('view_hidden_comments', 'Can view hidden comments'),
        )

    @property
    def short_text(self) -> str:
        """ Returns the first 40 characters of the post's text. """
        MAX_LENGTH = 40
        if len(self.text) > MAX_LENGTH:
            return self.text[:MAX_LENGTH] + '...'
        else:
            return self.text

    def __str__(self) -> str:
        return f"{self.author.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class PostReport(models.Model):
    MAX_REPORT_COUNT = 3

    post: Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports", verbose_name="post signalé")
    user: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name="reports", verbose_name="auteur du signalement")
    created_at = models.DateTimeField("date du signalement", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_report_post_user'),
        ]

        verbose_name = "signalement"
        verbose_name_plural = "signalements"

        permissions = (
            ('reset_reports', 'Can reset reports'),
            ('view_reports', 'Can view reports'),
        )

    def validate_unique(self, exclude: iter = None) -> None:
        """ Check you can't report the same post twice """
        if PostReport.objects.filter(post=self.post, user=self.user).exists():
            raise ValidationError("Vous avez déjà signalé ce post")
        super().validate_unique(exclude)

    def clean(self) -> None:
        """ Check you can't report your own post """
        if self.post.author == self.user:
            raise ValidationError("Vous ne pouvez pas signaler votre propre post")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ Override save method to prevent more than 3 reports per post """
        super().save(force_insert, force_update, using, update_fields)
        reports = PostReport.objects.filter(post=self.post)
        if reports >= self.MAX_REPORT_COUNT:
            self.post.status = self.post.HIDDEN
            self.post.save()

    def __repr__(self) -> str:
        return f'{self.post} - {self.user.username}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", verbose_name="post aimé")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="likes", verbose_name="utilisateur aimant")
    created_at = models.DateTimeField("date", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_like_post_user')
        ]

        verbose_name = "like"
        verbose_name_plural = "likes"

        permissions = (
            ('reset_likes', 'Can reset likes'),
            ('view_likes', 'Can view likes'),
        )

    def validate_unique(self, exclude: iter = None) -> None:
        """ Check you can't like the same post twice """
        if Like.objects.filter(post=self.post, user=self.user).exists():
            raise ValidationError("Vous avez déjà liké ce post")
        super().validate_unique(exclude)

    def __str__(self) -> str:
        return f'{self.post} - {self.user.username}'
