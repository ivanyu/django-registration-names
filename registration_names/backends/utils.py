from copy import deepcopy
from django.core.urlresolvers import RegexURLPattern
from django.conf.urls import url


def transform_registration_patters(patterns, new_backend):
    """
    Transform patterns declared in registration app to work with
    specified backend.
    """
    result = []
    for p in patterns:
        # Don't transform RegexURLResolver and ones which don't have 'backend'
        # argument specified.
        if (not isinstance(p, RegexURLPattern) or
            'backend' not in p.default_args):
            result.append(p)
            continue

        new_default_args = deepcopy(p.default_args)
        new_default_args['backend'] = new_backend        
        result.append(
            url(p.regex.pattern, p.callback, new_default_args, p.name))
    return result