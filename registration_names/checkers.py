"""
Usersnames checkers.
"""
import re

from django.core.exceptions import ImproperlyConfigured
from django.utils import six


class Checker(object):
    """
    The checker of usernames allowed.

    Initialized with a dictionary in the following format:

        root = {
            'control_type': 'allowed',

            'allowed': [
                'SimpleAllowed',
                ('re', 'i', 'Regexp!+allowed'),
            ],

            'prohibited': [
                'SimpleProhibited',
            ]
        }

    The first key is 'control_type' which can be 'disabled', 'allowed',
    'prohibited' or 'allowed_and_prohibited'.
    * With 'disabled' no check will be done, all passed usernames will be
    considered allowed.
    * With 'allowed' the 'allowed' list will be used to check if passed
    username is allowed.
    * With 'prohibited' all names will be considered allowed except those which
    explicitly prohibited by 'prohibited' list.
    * With 'allowed_and_prohibited' an username will be considered allowed only
    if it's aexplicitly llowed by 'allowed' list and not explicitly prohibited
    by 'prohibited' list.

    With each 'control_type' all correspondeing lists are required even in case
    they're empty.

    The format of the lists is the following. Each lists consists of two types
    of items: strings and regular expressions. Usersnames will be simply
    compared with string and matched with regexps. Regexps are set by 3-element
    tuples of strings:
    * The first element is a marker 're'.
    * The second element is keys. The only possible key now is 'i' of case
    insensitivity.
    * The third is a regexp pattern.

    Of course, it's possible to use 3-element lists or another suitable type
    instead of tuple.
    """

    __CONTROL_TYPE = 'control_type'
    __CONTROL_TYPE_ALLOWED = 'allowed'
    __CONTROL_TYPE_PROHIBITED = 'prohibited'
    __CONTROL_TYPE_ALLOWED_PROHIBITED = 'allowed_and_prohibited'
    __CONTROL_TYPE_DISABLED = 'disabled'

    def __init__(self, root=None):
        """
        Constructor.

        `root` - a configuration dictionary (e.g. from settings).
        The format is discribed early.
        """
        self.__control_type = None

        if root is None:
            return

        KEY_ALLOWED = 'allowed'
        KEY_PROHIBITED = 'prohibited'

        POSSIBLE_CONTROL_TYPES_STR = "'{}', '{}', '{}' and '{}'".format(
            self.__CONTROL_TYPE_ALLOWED,
            self.__CONTROL_TYPE_PROHIBITED,
            self.__CONTROL_TYPE_ALLOWED_PROHIBITED,
            self.__CONTROL_TYPE_DISABLED)

        if self.__CONTROL_TYPE not in root:
            raise ImproperlyConfigured(
                "'{}' key is expected. "
                "Possible values: {}.".format(
                    self.__CONTROL_TYPE, POSSIBLE_CONTROL_TYPES_STR))

        self.__control_type = root[self.__CONTROL_TYPE]

        if self.__control_type not in [self.__CONTROL_TYPE_ALLOWED,
                                       self.__CONTROL_TYPE_PROHIBITED,
                                       self.__CONTROL_TYPE_ALLOWED_PROHIBITED,
                                       self.__CONTROL_TYPE_DISABLED]:
            raise ImproperlyConfigured(
                "'{}' possible values: "
                "{}.".format(self.__CONTROL_TYPE, POSSIBLE_CONTROL_TYPES_STR))

        self.__allowed_str = None
        self.__allowed_re = None
        self.__prohibited_str = None
        self.__prohibited_re = None

        if (self.__control_type == self.__CONTROL_TYPE_ALLOWED or
                self.__control_type == self.__CONTROL_TYPE_ALLOWED_PROHIBITED):
            if KEY_ALLOWED not in root:
                raise ImproperlyConfigured(
                    "'{}' set to '{}' but '{}' "
                    "list not found.".format(self.__CONTROL_TYPE,
                                             root[self.__CONTROL_TYPE],
                                             KEY_ALLOWED))
            self.__allowed_str, self.__allowed_re = self.__parse_list(
                root[KEY_ALLOWED], KEY_ALLOWED)

        if (self.__control_type == self.__CONTROL_TYPE_PROHIBITED or
                self.__control_type == self.__CONTROL_TYPE_ALLOWED_PROHIBITED):
            if KEY_PROHIBITED not in root:
                raise ImproperlyConfigured(
                    "'{}' set to '{}' but '{}' "
                    "list not found.".format(self.__CONTROL_TYPE,
                                             self.__control_type,
                                             KEY_PROHIBITED))
            self.__prohibited_str, self.__prohibited_re = self.__parse_list(
                root[KEY_PROHIBITED], KEY_PROHIBITED)

    def __parse_list_element(self, list_name, element, element_n):
        """
        Parse element from the list with all necessary checks.

        `list_name` - the name of the list ('allowed', 'prohibited' or
        'allowed_and_prohibited').
        `element` - the element from the list to parse.
        `element_n` - the element's position in the list.
        """

        KEYS_STR = "'i'"

        if isinstance(element, six.string_types):
            return ('str', element,)

        # Element isn't a string - consider it as 3-element re-tuple or list.
        try:
            length = len(element)
        except TypeError:
            raise ImproperlyConfigured(
                "Elements of '{}' must be strings or 3-element "
                "tuples or lists. Element on position {}: '{}'.".format(
                    list_name, element_n, element))

        if length != 3:
            raise ImproperlyConfigured(
                "3-element tuple is expected in '{}' on position {}, "
                "'{}' given.".format(list_name, element_n, element))

        # The first must be a 're' string.
        if element[0] != 're':
            raise ImproperlyConfigured(
                "First element of tuple in '{}' on position {} must be 're', "
                "'{}' given.".format(list_name, element_n, element[0]))

        # The second must be a string with allowed keys.
        if not isinstance(element[1], six.string_types):
            raise ImproperlyConfigured(
                "Second element of tuple in '{}' on position {} must be "
                "a string with one of the keys: {}. '{}' given."
                "".format(list_name, element_n, KEYS_STR, element[1]))

        # The third must be a string.
        if not isinstance(element[2], six.string_types):
            raise ImproperlyConfigured(
                "Third element of tuple in '{}' on position {} must be "
                "a string.".format(list_name, element_n, KEYS_STR))

        re_flags = 0
        for k in element[1]:
            if k == 'i':
                re_flags |= re.I
            else:
                raise ImproperlyConfigured(
                    "Unknown key '{}' in '{}' on position {}. "
                    "Possible keys: {}."
                    "".format(k, list_name, element_n, KEYS_STR))

        return ('re', re.compile(element[2], re_flags),)

    def __parse_list(self, patterns_list, list_name):
        """
        Parse 'allowed', 'prohibited' or 'allowed_and_prohibited' list.

        `patterns_list` - the list.
        `list_name` - the name of the list.
        """

        # Common error - a string instead of a sequence of strings.
        if isinstance(patterns_list, six.string_types):
            raise ImproperlyConfigured(
                "The value of '{}' must be an sequence (list, tuple), "
                "not a single string.".format(list_name))

        # Catch non-iterables.
        try:
            iter(patterns_list)
        except TypeError:
            raise ImproperlyConfigured(
                "The value of '{}' must be an iterable sequence "
                "(list, tuple). '{}' given.".format(list_name, patterns_list))

        result_str = []
        result_re = []
        for i, p in enumerate(patterns_list):
            t, v = self.__parse_list_element(list_name, p, i)
            if t == 're':
                result_re.append(v)
            else:
                result_str.append(v)
        return result_str, result_re

    def __check_allowed(self):
        """
        Determine if checking of allowed is required.
        """

        return (self.__control_type == self.__CONTROL_TYPE_ALLOWED or
                self.__control_type == self.__CONTROL_TYPE_ALLOWED_PROHIBITED)

    def __check_prohibited(self):
        """
        Determine if checking of prohibited is required.
        """

        return (self.__control_type == self.__CONTROL_TYPE_PROHIBITED or
                self.__control_type == self.__CONTROL_TYPE_ALLOWED_PROHIBITED)

    def check(self, value):
        """
        Check passed `value` according to the checker's configuration.
        """

        if self.__control_type == self.__CONTROL_TYPE_DISABLED:
            return True

        allowed = True
        if self.__check_allowed():
            allowed = (value in self.__allowed_str)
            if not allowed:
                for r in self.__allowed_re:
                    if r.match(value):
                        allowed = True
                        break
        if not allowed:
            return False

        prohibited = False
        if self.__check_prohibited():
            prohibited = (value in self.__prohibited_str)
            if not prohibited:
                for r in self.__prohibited_re:
                    if r.match(value):
                        prohibited = True
                        break
        if prohibited:
            return False

        return True
