from django import template
register = template.Library()

@register.simple_tag()
def replaceItem(originalString, *args, **kwargs):
    return originalString.replace("-", " ")