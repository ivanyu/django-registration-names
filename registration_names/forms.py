from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm


class RegistrationNameControlForm(RegistrationForm):
    """
    Form for registering a new user account which checks username to be allowed
    for registeration.
    """

    def clean_username(self):
        username = super(RegistrationNameControlForm, self).clean_username()

        prohibited_msg = _("This username is prohibited.")

        prohibited_list = getattr(settings, 'REGISTRATION_NAMES_PROHIBITED', [])
        if username in prohibited_list:
            raise forms.ValidationError(prohibited_msg)
        else:
            return username
