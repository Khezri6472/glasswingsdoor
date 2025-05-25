from django import template

register = template.Library()

@register.filter
def Approved_Comment(comments):
    return comments.filter(status = 'a')

