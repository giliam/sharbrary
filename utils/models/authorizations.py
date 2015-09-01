# coding: utf-8
from django.views.generic.base import View
from django.core.exceptions import PermissionDenied

class CheckOwner(View):
    def dispatch(self, request, *args, **kwargs):
        # Checks that the class at least has the owner_field or it is bad configured.
        if not hasattr(self,'owner_field'):
            raise Exception, "No owner field specified in " + self.__class__.__name__ + " class."
        
        # Gets the moderation permission from the table name. Could be wrong.
        if not request.user.has_perm(self.get_object()._meta.db_table.replace('_','.') + "_moderate") and not is_related_to_object(request.user,self.get_object(),self.owner_field):
            raise PermissionDenied

        return super(CheckOwner, self).dispatch(request, *args, **kwargs)

def is_related_to_object(user, object_to_test, field_name, many=False):
    # Tests if field name sent is one field or many
    if isinstance(field_name, list) or isinstance(field_name, tuple):
        for field in field_name:
            if is_this_related_to(user,object_to_test,field):
                return True
        return False
    else:
        return is_this_related_to(user,object_to_test,field_name)

def is_this_related_to(user,object_to_test,field_name,many=False):
    # Must have either attribute or method of that name.
    if not hasattr(object_to_test,field_name):
        raise Exception, "This field " + field_name + " does not exist in " + object_to_test.__class__.__name__ + " class." 
    
    attr = getattr(object_to_test, field_name)
    # Either the attribute is callable and then the use must be in the call of it or it is not callable and the user must be in the not call of it
    if many and ( not callable(attr) and user not in attr or callable(attr) and user not in attr() ):
        return False
    elif not many and ( not callable(attr) and user != attr or callable(attr) and user != attr()):
        return False
    return True