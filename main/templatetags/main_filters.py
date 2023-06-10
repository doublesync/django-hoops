from django import template
from ..league.extra import convert as league_converters
from ..league.player import style as player_style

register = template.Library()


@register.filter(name="addclass")
def addclass(value, arg):
    return value.as_widget(attrs={"class": arg})


@register.filter(name="addid")
def addid(value, arg):
    return value.as_widget(attrs={"id": arg})


@register.filter(name="addplaceholder")
def addplaceholder(value, arg):
    return value.as_widget(attrs={"placeholder": arg})


@register.filter(name="getattr")
def get_attribute(obj, attr):
    return getattr(obj, attr)


@register.filter(name="getvalue")
def get_value(obj, key):
    return obj[key]


@register.filter(name="americanheight")
def american_height(value):
    return league_converters.convert_to_height(value)


@register.filter(name="getage")
def get_age(value):
    return league_converters.format_years_played(value)

@register.filter(name="getstyle")
def get_style(obj, key):
    response = get_value(obj, key)
    return response["value"]

@register.filter(name="int")
def int_filter(value):
    return int(value)

@register.filter(name="lengthinc")
def lengthinc(value):
    return len(value) + 1