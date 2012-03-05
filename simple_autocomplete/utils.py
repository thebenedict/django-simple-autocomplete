from django.db.models.fields import FieldDoesNotExist, CharField
from django.conf import settings


def get_search_fieldname(model):
    # If 'search_field' for the model is specified in settings, use it,
    # else if the model has field 'title' then use that, else use
    # the first CharField on model
    try:
        key = "%s" % model._meta
        return getattr(settings, 'SIMPLE_AUTOCOMPLETE',
                {})[key]['search_field']
    except KeyError:
        fieldname = ''
    try:
        model._meta.get_field_by_name('title')
        fieldname = 'title'
    except FieldDoesNotExist:
        for field in model._meta.fields:
            if isinstance(field, CharField):
                fieldname = field.name
                break
    if not fieldname:
        raise RuntimeError("Cannot determine fieldname")
    return fieldname


def get_threshold_for_model(model):
    key = '%s.%s' % (model._meta.app_label, model._meta.module_name)
    return getattr(settings, 'SIMPLE_AUTOCOMPLETE', {}).get(
        key, {}).get('threshold', None
    )
