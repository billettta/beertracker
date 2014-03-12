from django import template
from decimal import *

register = template.Library()

@register.filter    
def subtract(value, arg):
    try:
        returnVal = value - arg
    except:
        returnVal = None
    return returnVal

@register.filter    
def multiply(value, arg):
    try:
        arg1 = Decimal(value)
        arg2 = Decimal(arg)
        returnVal = arg1 * arg2
    except:
        returnVal = None
    return returnVal

@register.filter    
def divide(value, arg):
    try:
        arg1 = Decimal(value)
        arg2 = Decimal(arg)
        returnVal = arg1 / arg2
    except:
        returnVal = None
    return returnVal

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
