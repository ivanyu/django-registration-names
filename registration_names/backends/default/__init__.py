from registration.backends.default import DefaultBackend as StdDefaultBackend

from registration_names.forms import RegistrationNameControlForm


class DefaultBackend(StdDefaultBackend):
    """
    A registration backend which inherited from django-registration
    `DefaultBackend` and replaces the registration form with
    `RegistrationNameControlForm`.
    """

    def get_form_class(self, request):
        return RegistrationNameControlForm