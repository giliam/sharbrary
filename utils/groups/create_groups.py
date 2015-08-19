# -*- coding: utf-8 -*-
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.db import models, migrations

# Mode of permissing
INCLUDING_MODE = "including"
EXCLUDING_MODE = "excluding"

# Permissions that are authorized for reading
AUTHORIZED_READONLY_MODELS = {
    "__mode__":INCLUDING_MODE,
    "author":["list"],
    "editor":["list"],
    "theme":["list"],
    "period":["list"],
    "book":["list","detail"],
    "lending":["list"],
    "ownership":[],
    "profile":["show","list"],
}

# Models that are authorized for permissions by standard users
# The values associated to the key are the excluded permissions
AUTHORIZED_STANDARD_MODELS = {
    "__mode__":EXCLUDING_MODE,
    "author":[""],
    "editor":[],
    "theme":[],
    "period":[],
    "book":["remove_from_all_libraries"],
    "lending":[],
    "ownership":[],
    "profile":[],
}
def associate_perms(group,perms,perms_authorized):
    permissing_mode = perms_authorized["__mode__"]
    for perm in perms.all(): 
        parts = perm.codename.split("_",1)
        if len(parts) > 1:
            model = parts[0]
            action = parts[1]
            if ( permissing_mode == EXCLUDING_MODE and model in perms_authorized.keys() and not action in perms_authorized[model] ) or ( permissing_mode == INCLUDING_MODE and model in perms_authorized.keys() and action in perms_authorized[model] ):
                group.permissions.add(perm)
    group.save()

def add_groups(*args,**kargs):
    perms = Permission.objects.filter(Q(content_type__app_label='library')|Q(content_type__app_label='sharing'))
    created = True
    #READ ONLY Group
    # Which can display but not do anything.
    group, created = Group.objects.get_or_create(name='read_only')   
    if created:
        associate_perms(group,perms,AUTHORIZED_READONLY_MODELS)
        print 'read_only_user group has been successfully created'

    #STANDARD Group
    # Which can do almost everything.
    group, created = Group.objects.get_or_create(name='standard_user') 
    if created:
        associate_perms(group,perms,AUTHORIZED_STANDARD_MODELS)
        print 'standard_user group has been successfully created'
