# coding: utf8
from django.http import Http404
from django.contrib.contenttypes.models import ContentType

def get_content_type(*args, **kwargs):
    return ContentType.objects.get(*args, **kwargs)

def get_content_type_or_404(*args, **kwargs):
    """ simple return content_type of given model's application"""
    try:
        return get_content_type(*args, **kwargs)        
    except:
        raise Http404("There is no such content type with given object")

def get_content_type_or_None(*args, **kwargs):
    try:
        return get_content_type(*args, **kwargs)
    except:
        return None

def parse_perms(perms, app, model):
    _perms = []
    for p in perms:
        _perms.append(p.format(app=app, model=model))
    return _perms

def get_description(callable_object):
    if callable(callable_object):
        if hasattr(callable_object, 'short_description'):
            return callable_object.short_description
        else:
            return callable_object.__name__.replace('_', ' ')
    else:
        return None
