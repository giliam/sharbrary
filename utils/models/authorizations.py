# coding: utf-8
from django.core.exceptions import PermissionDenied

def is_owner(user, object_to_test, field_name, many=False):
    if many and user not in getattr(object_to_test, field_name):
        raise PermissionDenied
        return False
    elif not many and user == getattr(object_to_test, field_name):
        raise PermissionDenied
        return False
    return True