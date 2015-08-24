from django import template

register = template.Library()

@register.filter(name='keyvalue')
def keyvalue(dictionary, key):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return None