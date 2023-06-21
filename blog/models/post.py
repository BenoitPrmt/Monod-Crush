import logging

from django.db import models

from authentication.models import CustomUser

log = logging.getLogger(__name__)


class Post(models.Model):
    class PostStatus(models.TextChoices):
        NORMAL = 'N', 'Normal'
        AWAITING_VERIFICATION = 'A', 'En attente de vérification'
        HIDDEN = 'H', 'Masqué'

    VISIBLE_STATUSES = [PostStatus.NORMAL]

    text = models.TextField("contenu du post", max_length=500, help_text="Contenu du post")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts', verbose_name='Auteur')
    status = models.CharField("état", choices=PostStatus.choices, default=PostStatus.NORMAL, max_length=1)
    is_anonymous = models.BooleanField("post anonyme", default=True, help_text="Indique si le post est anonyme ou non")
    updated_at = models.DateTimeField("dernière modification", auto_now=True)
    created_at = models.DateTimeField("date de création", auto_now_add=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

        permissions = (
            # user permission
            ("create_posts", "Peut créer des posts"),
            ('edit_own_posts', 'Peut modifier ses propres posts'),
            ('delete_own_posts', 'Peut supprimer ses propres posts'),

            # moderator permission
            ('hide_posts_from_other_users', "Peut masquer des posts (sans voir l'auteur)"),
            ('delete_posts_from_other_users', "Peut supprimer les posts des autres (sans voir l'auteur)"),

            # admin permission
            ("view_posts_details", "Peut voir les détails des posts (dont l'auteur)"),
        )

        default_permissions = ()

    def reset_report(self) -> None:
        """ Reset all reports for this post. """
        self.reports.all().delete()

    @property
    def nb_of_likes(self) -> int:
        """ Return the number of likes for this post. """
        return self.likes.count()

    @property
    def nb_of_comments(self) -> int:
        """ Return the number of comments for this post. """
        return self.comments.count()

    @property
    def nb_of_reports(self) -> int:
        """ Return the number of reports for this post. """
        return self.reports.count()

    @property
    def short_text(self) -> str:
        """ Returns the first 40 characters of the post's text. """
        MAX_LENGTH = 37  # 40 characters - 3 dots
        if len(self.text) > MAX_LENGTH:
            return self.text[:MAX_LENGTH] + '...'
        else:
            return self.text

    def __str__(self) -> str:
        return f"{self.id} - {self.author.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
