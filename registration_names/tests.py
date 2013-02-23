import os
import sys
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'registration_names.settings'

from unittest import TestCase

from django.core.exceptions import ImproperlyConfigured
#from django.conf import settings

from checkers import Checker


class IncorrectConfigTests(TestCase):
    def setUp(self):
        pass

    def test_empty_dic(self):
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({})
        self.assertEqual(
            e.exception.message,
            "'control_type' key is expected. "
            "Possible values: 'allowed', 'prohibited', "
            "'allowed_and_prohibited' and 'disabled'.")

    def test_control_type_empty(self):
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': ''})
        self.assertEqual(
            e.exception.message,
            "'control_type' possible values: 'allowed', 'prohibited', "
            "'allowed_and_prohibited' and 'disabled'.")

        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': None})
        self.assertEqual(
            e.exception.message,
            "'control_type' possible values: 'allowed', 'prohibited', "
            "'allowed_and_prohibited' and 'disabled'.")

    def test_control_type_invalid_type(self):
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 123})
        self.assertEqual(
            e.exception.message,
            "'control_type' possible values: 'allowed', 'prohibited', "
            "'allowed_and_prohibited' and 'disabled'.")

    def test_allowed_wo_list(self):
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'allowed'})
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'allowed' but 'allowed' list not found.")

        # With prohibited-list
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'allowed', 'prohibited': []})
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'allowed' but 'allowed' list not found.")

        # With prohibited-list
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({
                'control_type': 'allowed_and_prohibited',
                'prohibited': []
            })
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'allowed_and_prohibited' "
            "but 'allowed' list not found.")

    def test_allowed_incorrect_list_type(self):
        # Incorrect type instead of list.
        root = {
            'control_type': 'allowed',
            'allowed': 123,
        }
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker(root)
        self.assertEqual(
            e.exception.message,
            "The value of 'allowed' must be an iterable sequence "
            "(list, tuple). '123' given.")

        # String instead of list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'allowed', 'allowed': 'Name'})
        self.assertEqual(
            e.exception.message,
            "The value of 'allowed' must be an sequence (list, tuple), "
            "not a single string.")

    def test_prohibited_wo_list(self):
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'prohibited'})
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'prohibited' "
            "but 'prohibited' list not found.")

        # With allowed-list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'prohibited', 'allowed': []})
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'prohibited' "
            "but 'prohibited' list not found.")

        # With allowed-list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'allowed_and_prohibited', 'allowed': []})
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'allowed_and_prohibited' "
            "but 'prohibited' list not found.")

    def test_prohibited_incorrect_list_type(self):
        # Incorrect type instead of list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({
                'control_type': 'prohibited',
                'prohibited': 123,
            })
        self.assertEqual(
            e.exception.message,
            "The value of 'prohibited' must be an iterable sequence "
            "(list, tuple). '123' given.")

        # String instead of list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'prohibited', 'prohibited': 'Name'})
        self.assertEqual(
            e.exception.message,
            "The value of 'prohibited' must be an sequence (list, tuple), "
            "not a single string.")

    def test_allowed_and_prohibited(self):
        # Without any list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'allowed_and_prohibited'})
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'allowed_and_prohibited' "
            "but 'allowed' list not found.")

        # Without prohibited list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({
                'control_type': 'allowed_and_prohibited',
                'allowed': [],
            })
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'allowed_and_prohibited' "
            "but 'prohibited' list not found.")

        # Without allowed list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({
                'control_type': 'allowed_and_prohibited',
                'prohibited': [],
            })
        self.assertEqual(
            e.exception.message,
            "'control_type' set to 'allowed_and_prohibited' "
            "but 'allowed' list not found.")

    def test_str_and_re(self):
        # Non-string ang non-tuple/list.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'prohibited', 'prohibited': [123]})
        self.assertEqual(
            e.exception.message,
            "Elements of 'prohibited' must be strings or 3-element tuples "
            "or lists. Element on position 0: '123'.")

        # Incorrect tuple length.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'prohibited', 'prohibited': [(1,)]})
        self.assertEqual(
            e.exception.message,
            "3-element tuple is expected in 'prohibited' on position 0, "
            "'(1,)' given.")

        # Incorrect 1st element.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({'control_type': 'prohibited', 'prohibited': [[1, 2, 3]]})
        self.assertEqual(
            e.exception.message,
            "First element of tuple in 'prohibited' on position 0 "
            "must be 're', '1' given.")

        # Incorrect 2nd element.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({
                'control_type': 'prohibited',
                'prohibited': [['re', 2, 3]]
            })
        self.assertEqual(
            e.exception.message,
            "Second element of tuple in 'prohibited' on position 0 must be "
            "a string with one of the keys: 'i'. '2' given.")

        # Incorrect 3rd element.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({
                'control_type': 'prohibited',
                'prohibited': [['re', '', 3]]
            })
        self.assertEqual(
            e.exception.message,
            "Third element of tuple in 'prohibited' on "
            "position 0 must be a string.")

        # Unknown keys.
        with self.assertRaises(ImproperlyConfigured) as e:
            Checker({
                'control_type': 'prohibited',
                'prohibited': [['re', 'qwe', 'pattern']]
            })
        self.assertEqual(
            e.exception.message,
            "Unknown key 'q' in 'prohibited' on position 0. "
            "Possible keys: 'i'.")


class CorrectConfigTests(TestCase):
    def test_disabled(self):
        c = Checker({'control_type': 'disabled'})
        self.assertEqual(c.check("Some name."), True)

        # Strange keys.
        c = Checker({'control_type': 'disabled', 'asdasd': None})
        self.assertEqual(c.check("Some name."), True)

        # Error in lists.
        c = Checker({'control_type': 'disabled', 'allowed': None})
        self.assertEqual(c.check("Some name."), True)

        # Prohibited list.
        root = {
            'control_type': 'disabled',
            'allowed': [],
            'prohibited': ["Some name."]
        }
        c = Checker(root)
        self.assertEqual(c.check("Some name."), True)

    def test_allowed_only(self):
        root = {
            'control_type': 'allowed',
            'allowed': [
                'Explicit name.',
                ('re', '', 'pA+ttern'),
                ('re', 'i', 'sTrAnGe'),
            ]
        }
        c = Checker(root)
        self.assertEqual(c.check("not allowed"), False)
        self.assertEqual(c.check("pattern"), False)  # Lower-case 'a'.

        self.assertEqual(c.check("Explicit name."), True)
        self.assertEqual(c.check("pAttern"), True)
        self.assertEqual(c.check("pAAAttern"), True)

        self.assertEqual(c.check("strange"), True)
        self.assertEqual(c.check("STRANGE"), True)

    def test_prohibited_only(self):
        root = {
            'control_type': 'prohibited',
            'prohibited': [
                'Explicit name.',
                ('re', '', 'pA+ttern'),
                ('re', 'i', 'sTrAnGe'),
            ]
        }
        c = Checker(root)
        self.assertEqual(c.check("allowed"), True)
        self.assertEqual(c.check("pattern"), True)  # Lower-case 'a'.

        self.assertEqual(c.check("Explicit name."), False)
        self.assertEqual(c.check("pAttern"), False)
        self.assertEqual(c.check("pAAAttern"), False)

        self.assertEqual(c.check("strange"), False)
        self.assertEqual(c.check("STRANGE"), False)

    def test_allowed_and_prohibited(self):
        root = {
            'control_type': 'allowed_and_prohibited',
            'allowed': [
                'Explicit name.',
                ('re', '', 'pA+ttern'),
                ('re', 'i', 'sTrAnGe'),
            ],
            'prohibited': [
                'pAAttern',
                ('re', '', 'sT.*')
            ]
        }
        c = Checker(root)
        self.assertEqual(c.check("not allowed"), False)
        self.assertEqual(c.check("pattern"), False)  # Lower-case 'a'.

        self.assertEqual(c.check("Explicit name."), True)
        self.assertEqual(c.check("pAttern"), True)
        self.assertEqual(c.check("pAAttern"), False)
        self.assertEqual(c.check("pAAAttern"), True)

        self.assertEqual(c.check("sTrange"), False)
        self.assertEqual(c.check("strange"), True)
        self.assertEqual(c.check("STRANGE"), True)
