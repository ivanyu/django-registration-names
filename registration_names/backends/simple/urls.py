"""
URLconf which uses django-registration's one but changes backend argument
to `registration_names.backends.simple.SimpleBackend`.
"""


from __future__ import absolute_import
from registration.backends.default.urls import urlpatterns as std_urlpatterns

from ..utils import transform_registration_patters


urlpatterns = transform_registration_patters(std_urlpatterns,
    'registration_names.backends.simple.SimpleBackend')
