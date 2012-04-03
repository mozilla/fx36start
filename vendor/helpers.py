def f(string, *args, **kwargs):
    """
    Uses ``str.format`` for string interpolation.

    >>> {{ "{0} arguments and {x} arguments"|f('positional', x='keyword') }}
    "positional arguments and keyword arguments"
    """
    string = unicode(string)
    return string.format(*args, **kwargs)


def load_filters(env):
    """Load all filters and functions into jinja2 environment 'env'."""
    env.filters['f'] = f  # |f(...)