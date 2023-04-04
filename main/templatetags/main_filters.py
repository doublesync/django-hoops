from django import template

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
