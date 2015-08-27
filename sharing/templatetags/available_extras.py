from django import template

from utils.models.availability import is_lending_possible, is_queueing_possible

register = template.Library()

@register.filter(name='can_queue', takes_context=True)
def can_queue(book_copy, user):
    return not is_queueing_possible(book_copy,user)