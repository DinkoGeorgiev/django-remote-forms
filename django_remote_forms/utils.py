from django.utils.functional import Promise
from django.utils.encoding import force_text as force_unicode
from django.http.request import QueryDict


def resolve_promise(o):
    if isinstance(o, dict):
        if isinstance(o, QueryDict):
            o = o.copy()
        for k, v in o.items():
            o[k] = resolve_promise(v)
    elif isinstance(o, (list, tuple)):
        o = [resolve_promise(x) for x in o]
    elif isinstance(o, Promise):
        try:
            o = force_unicode(o)
        except:
            # Item could be a lazy tuple or list
            try:
                o = [resolve_promise(x) for x in o]
            except:
                raise Exception('Unable to resolve lazy object %s' % o)
    elif callable(o):
        o = o()

    return o
