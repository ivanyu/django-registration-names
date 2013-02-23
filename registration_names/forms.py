from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm

from checkers import Checker


class RegistrationNameControlForm(RegistrationForm):
    """
    Form for registering a new user account which checks username to be allowed
    for registeration.
    """

    def clean_username(self):
        ROOT_CONFIG = 'REGISTRATION_NAMES'

        checker = Checker(getattr(settings, ROOT_CONFIG, None))
        username = super(RegistrationNameControlForm, self).clean_username()

        if checker.check(username):
            return username
        else:
            raise forms.ValidationError(_("This username isn't allowed."))
