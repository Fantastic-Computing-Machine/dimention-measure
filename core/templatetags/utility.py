from django import template

import math

register = template.Library()


@register.simple_tag()
def replaceItem(originalString: str, *args, **kwargs) -> str:
    return originalString.replace("-", " ")


@register.simple_tag()
def formatFloat(value: str, n=2) -> str:
    value = str(math.floor(float(value) * 10**n) / 10**n)
    # format the number to international format
    value = "{:,}".format(float(value))
    return value


@register.simple_tag()
def meter2feet(meters: str) -> str:
    # Convert meters to feet
    feet = float(meters) * 3.28084
    inches = round((feet - int(feet)) * 12, 2)
    return f"{int(feet)}' {inches}\""
