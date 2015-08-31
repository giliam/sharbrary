# coding: utf-8
from django.views.generic.base import View
from django.core.exceptions import PermissionDenied

class CheckOwner(View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self,'owner_field'):
            raise Exception, "No owner field specified in " + self.__class__.__name__ + " class."

        if not is_owner_of(request.user,self.get_object(),self.owner_field):
            raise PermissionDenied

        return super(CheckOwner, self).dispatch(request, *args, **kwargs)

def is_owner_of(user, object_to_test, field_name, many=False):
    if many and user not in getattr(object_to_test, field_name):
        return False
    elif not many and user != getattr(object_to_test, field_name):
        return False
    return True