from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from registration.forms import RegistrationForm


class RegistrationNameControlForm(RegistrationForm):
    """
    Form for registering a new user account which checks username to be allowed
    for registeration.
    """

    def __handle_prohibited(self, username):
        prohibited_list = getattr(settings, 'REGISTRATION_NAMES_PROHIBITED', [])
        if username in prohibited_list:
            raise forms.ValidationError(_("This username isn't allowed."))
        else:
            return username

    def __handle_allowed(self, username):
        allowed_list = getattr(settings, 'REGISTRATION_NAMES_ALLOWED', [])
        if username not in allowed_list:
            raise forms.ValidationError(_("This username isn't allowed."))
        else:
            return username

    def clean_username(self):
        names_ctrl = getattr(settings, 'REGISTRATION_NAMES_CONTROL_TYPE', [])
        if names_ctrl not in ('prohibited', 'allowed', ):
            raise ImproperlyConfigured(
                "REGISTRATION_NAMES_CONTROL_TYPE can only have value "
                "'prohibited' or 'allowed'.")
        
        username = super(RegistrationNameControlForm, self).clean_username()
        if names_ctrl == 'prohibited':
            return self.__handle_prohibited(username)
        else:
            return self.__handle_allowed(username)
