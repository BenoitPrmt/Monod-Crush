from django.core.exceptions import ValidationError
from django.db import models

from authentication.models import CustomUser
from blog.models.post import Post


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", verbose_name="post aimé")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes", verbose_name="auteur du like")
    created_at = models.DateTimeField("date", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_like_post_user')
        ]

        verbose_name = "like"
        verbose_name_plural = "likes"

        permissions = (
            # user permission
            ("like_posts", "Peut aimer des posts"),
        )

        default_permissions = ()

    def validate_unique(self, exclude: iter = None) -> None:
        """ Check you can't like the same post twice """
        if Like.objects.filter(post=self.post, user=self.user).exists():
            raise ValidationError("Vous avez déjà liké ce post")
        super().validate_unique(exclude)

    def __str__(self) -> str:
        return f'{self.post} - {self.user.username}'
