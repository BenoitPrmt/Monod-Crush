from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_\-.]{4,20}$',
        message='Le nom d\'utilisateur doit être composé de 4 à 20 caractères alphanumériques, '
                'des tirets, des underscores ou des points.',
        code='invalid'
)


def date_of_birth_validator(date_of_birth: date):
    """ Check if date_of_birth is coherent """
    if date_of_birth > date.today():
        raise ValidationError("Tu n'es pas encore né(e) ?")
    elif date_of_birth.year < 1930:
        raise ValidationError(f"Arrête, tu n'as pas {date.today().year - date_of_birth.year} ans")
    elif date_of_birth + timedelta(days=365.2425 * 13) > date.today():
        days_remaining = (date_of_birth + timedelta(days=365.2425 * 13)) - date.today()
        raise ValidationError(f"Tu est encore trop jeune, il te reste {days_remaining.days} jours à attendre")


instagram_validator = RegexValidator(
        regex=r'^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$',
        message="Le nom du d'utilisateur instagram ne correspond pas à la norme.",
        code='invalid'
)


twitter_validator = RegexValidator(
        regex=r'^[A-Za-z0-9_]{1,15}$',
        message="Le nom du d'utilisateur twitter ne correspond pas à la norme.",
        code='invalid'
)
