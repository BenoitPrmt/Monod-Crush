import re
import string
from typing import Tuple

from flask import Blueprint

from flaskr.db import get_db

bp = Blueprint('auth_helper', __name__)

def check_email(email: str) -> Tuple[bool, str]:
    """ Check if the email is true """

    if re.search('@', email) is None or re.search('.', email) is None:
        return False, "Votre email doit contenir un @ et un ."

    if not re.match(r'^[A-Za-z][A-Za-z0-9_-]+$', email):
        return False, "Votre email doit commencer par une lettre"

    return True, ""

def check_firstname(firstname: str) -> Tuple[bool, str]:
    """Check firstname"""

    alpha = string.ascii_letters
    if not firstname.startswith(tuple(alpha)):
        return False, "Votre prénom doit commencer par une lettre"

    if len(firstname) < 3:
        return False, "Votre prénom doit contenir au moins 3 caractères"
    elif len(firstname) > 20:
        return False, "Votre prénom doit contenir 20 caractères maximum"

    return True, ""

def check_bio(bio: str) -> Tuple[bool, str]:
    """ Check bio"""

    if len(bio) > 300:
        return False, "Votre bio doit contenir 300 caractères maximum"

    return True, ""

def check_class_level(class_level: str) -> Tuple[bool, str]:
    """ Check class level"""

    if int(class_level) < 0 or int(class_level) > 2:
        return False, "Le niveau de classe doit être compris entre 0 et 2"

    return True, ""

def check_class_number(class_number: str) -> Tuple[bool, str]:
    """ Check class number"""

    if int(class_number) < 1 or int(class_number) > 18:
        return False, "Le numéro de classe doit être compris entre 1 et 18"

    return True, ""

def check_social(social: str) -> Tuple[bool, str]:
    """ Check social"""

    if social == "":
        return False, "Votre pseudo doit être renseigné"

    if re.search(':', social) is not None or re.search('/', social) is not None:
        return False, "Votre réseau social doit être seulement votre nom d'utilisateur et ne doit pas contenir un / ni un :"

    if len(social) < 3:
        return False, "Votre compte social doit contenir 3 caractères minimum"

    if len(social) > 20:
        return False, "Votre compte social doit contenir 20 caractères maximum"

    return True, ""

def check_website(website: str) -> Tuple[bool, str]:
    """ Check website"""

    if re.search('http', website) is None:
        return False, "Votre site web doit commencer par http ou https"

    if len(website) > 200:
        return False, "Votre site web doit contenir 200 caractères maximum"

    return True, ""