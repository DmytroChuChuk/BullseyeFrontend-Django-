# app/templatetags/util.py
from django import template

register = template.Library()

@register.filter(name='get_type')
def get_type(value):
    return type(value)

@register.filter(name='ifinlist')
def ifinlist(value, list):
   return value in list

@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value

def update_var(value):
    data = value
    return data

register.filter('update_var', update_var)