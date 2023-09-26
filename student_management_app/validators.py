from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

from .models import CustomUser


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if password is None:
            raise ValidationError(_("The password can not be empty."))
        if len(password) < 8:
            raise ValidationError(_("The password must be at least 8 characters long."))
        if len(password) > 20:
            raise ValidationError(_("The password must be at most 20 characters long."))
        if not re.search(r"[a-z]", password):
            raise ValidationError(_("The password must contain at least one lowercase letter."))
        if not re.search(r"[A-Z]", password):
            raise ValidationError(_("The password must contain at least one uppercase letter."))
        if not re.search(r"\d", password):
            raise ValidationError(_("The password must contain at least one digit."))
        if not re.search(r"[?!@#$%^&*(){}\-\[\]~:;'\"./\\_]", password):
            raise ValidationError(_("The password must contain at least one special letter."))

        return password

    def get_help_text(self):
        return _("Your password must contain at least 8 characters including one uppercase character, "
                 "one lowercase character, one digit and one special character.")


def handle_password_validation(password):
    try:
        password_validator = CustomPasswordValidator()
        password_validator.validate(password)
        return None  # Return None if password validation succeeds
    except ValidationError as e:
        return str(e)[2:-2]


def validate_email_address(email_address):
    """Validates an email address."""
    if email_address is None:
        return False
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+.[a-zA-Z]+$')
    if not email_regex.match(email_address):
        return False
    return True


class CustomUserExistenceValidator:
    def validate(self, email, username):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_("A user with this email address already exists."))
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(_("A user with that username already exists."))


def handle_user_error(email, username):
    try:
        validator = CustomUserExistenceValidator()
        validator.validate(email, username)
        return None
    except ValidationError as e:
        return str(e)[2:-2]
