from django import template
from decimal import *

register = template.Library()

@register.filter    
def subtract(value, arg):
    return value - arg

@register.filter    
def multiply(value, arg):
    arg1 = Decimal(value)
    arg2 = Decimal(arg)
    return arg1 * arg2

@register.filter    
def divide(value, arg):
    arg1 = Decimal(value)
    arg2 = Decimal(arg)
    return arg1 / arg2

@register.inclusion_tag('tracker/beerTable.html')
def beerTable(beers, **kwargs):
    if kwargs['orderBy'] != "":
        orderBy = kwargs['orderBy']
    else:
        orderBy = kwargs['defaultOrderBy']
    return {'beers' : beers, 'orderBy' : orderBy }

@register.inclusion_tag('tracker/breweryTable.html')
def breweryTable(breweries, **kwargs):
    if kwargs['orderBy'] != "":
        orderBy = kwargs['orderBy']
    else:
        orderBy = kwargs['defaultOrderBy']
    return {'breweries' : breweries, 'orderBy' : orderBy }

@register.inclusion_tag('tracker/styleTable.html')
def styleTable(styles, **kwargs):
    if kwargs['orderBy'] != "":
        orderBy = kwargs['orderBy']
    else:
        orderBy = kwargs['defaultOrderBy']
    return {'styles' : styles, 'orderBy' : orderBy }

@register.inclusion_tag('tracker/paginatorNumbers.html')
def paginateNumbers(currentPage, **kwargs):
    if kwargs['orderBy'] != "":
        orderBy = kwargs['orderBy']
    else:
        orderBy = kwargs['defaultOrderBy']
    return {'activePage' : currentPage, 'orderBy' : orderBy }
