from registration.backends.simple import SimpleBackend as StdSimpleBackend

from registration_names.forms import RegistrationNameControlForm


class SimpleBackend(StdSimpleBackend):
    """
    A registration backend which inherited from django-registration
    `SimpleBackend` and replaces the registration form with
    `RegistrationNameControlForm`.
    """
    
    def get_form_class(self, request):
        return RegistrationNameControlForm