django-registration-names
=========================

A way to control allowed and prohibited user names for registration with
*django-registration*.

The application provides tools (forms, backends, predefined URLs)
to help you define which user names are allowed to register in your project
and which are prohibited.

You may want to prohibit registration of user names which are "system" in
your project, e.g. 'add', 'user', 'profile' etc.

### Installation
The application can be installed by *setup.py*:

    python setup.py install

Or by using *pip*:

    pip install django-registration-names

Also you can simply place *registration* directory or symlink to it somewhere
on your PYTHON_PATH.

### Using

The application is coupled with *django-registration* application, so you need
it to be installed.

To use *django-registration-names* in your Django project add it to your
**INSTALLED\_APPS**:

    INSTALLED_APPS = (
        # other 
        'registration',
        'registration_names',
        # other 
    )

After that you can include URLs in project's URLconf, like you'd do with
*django-registration*:

    (r'^accounts/', include('registration_names.backends.default.urls')),

Of course, you can also redefine URLs, make your own backends and forms using
classes provided. In general, you can act like you'd act with
*django-registration* except that user names will be checked before
registration.

### Configuration

The main settings key is **REGISTRATION\_NAMES**. The format is the following:

    REGISTRATION_NAMES = {
        "control_type": "allowed",

        "allowed": [
            "SimpleAllowed",
            ("re", "i", "Regexp!+allowed"),
        ],

        "prohibited": [
            "SimpleProhibited",
        ],
    }

The first key is **control\_type** which can be *disabled*, *allowed*,
*prohibited* or *allowed_and_prohibited*.
* With *disabled* no check will be done, all passed usernames will be
considered allowed.
* With *allowed* the *allowed* list will be used to check if passed
username is allowed.
* With *prohibited* all names will be considered allowed except those which
explicitly prohibited by *prohibited* list.
* With *allowed_and_prohibited* an username will be considered allowed only
if it's aexplicitly llowed by *allowed* list and not explicitly prohibited
by *prohibited* list.

With each **control\_type** all correspondeing lists are required even in case
they're empty.

The format of the lists is the following. Each lists consists of two types
of items: strings and regular expressions. Usersnames will be simply
compared with string and matched with regexps. Regexps are set by 3-element
tuples of strings:
* The first element is a marker *re*.
* The second element is keys. The only possible key now is *i* of case
insensitivity.
* The third is a regexp pattern.

Of course, it's possible to use 3-element lists or another suitable type
instead of tuple.

### License
**MIT License**  
See LICENSE.txt

### Contributors
Project initially started by Ivan Yurchenko (ivan0yurchenko@gmail.com)