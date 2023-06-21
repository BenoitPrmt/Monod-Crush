import logging

from django.db import models

from authentication.models import CustomUser
from blog.models.post import Post

log = logging.getLogger(__name__)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="post")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments", verbose_name='auteur')
    text = models.TextField(max_length=300)
    is_anonymous = models.BooleanField("commentaire anonyme", default=True)
    created_at = models.DateTimeField("date de création", auto_now_add=True)

    class Meta:
        verbose_name = "commentaire"
        verbose_name_plural = "commentaires"

        permissions = (
            # user permission
            ("add_comments", "Peut ajouter des commentaires"),
            ("delete_own_comments", "Peut supprimer ses commentaires"),

            # moderator permission
            ("delete_comments_from_other_users", "Peut supprimer les commentaires des autres (sans voir l'auteur)"),

            # admin permission
            ("view_comments_details", "Peut voir les détails des commentaires (dont l'auteur)"),
        )

        default_permissions = ()

    @property
    def short_text(self) -> str:
        """ Returns the first 40 characters of the post's text. """
        MAX_LENGTH = 37  # 40 characters - 3 dots
        if len(self.text) > MAX_LENGTH:
            return self.text[:MAX_LENGTH] + '...'
        else:
            return self.text

    def __str__(self) -> str:
        return f"{self.author.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
