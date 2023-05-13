from django import template

import math

register = template.Library()


@register.simple_tag()
def replaceItem(originalString, *args, **kwargs):
    return originalString.replace("-", " ")


@register.simple_tag()
def formatFloat(value, n=2):
    value = str(math.floor(float(value) * 10 ** n) / 10 ** n)
    # format the number to international format
    value = "{:,}".format(float(value))
    return value
