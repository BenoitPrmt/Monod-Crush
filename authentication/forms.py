from django.contrib.auth.forms import UserCreationForm

from authentication.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('date_of_birth',)
