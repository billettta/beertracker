from django import template

register = template.Library()

@register.filter    
def subtract(value, arg):
    return value - arg

@register.inclusion_tag('tracker/beerTable.html')
def beerTable(beers, **kwargs):
    if kwargs['orderBy'] != "":
        orderBy = kwargs['orderBy']
    else:
        orderBy = kwargs['defaultOrderBy']
    return {'beers' : beers, 'orderBy' : orderBy }

@register.inclusion_tag('tracker/paginatorNumbers.html')
def paginateNumbers(currentPage, **kwargs):
    if kwargs['orderBy'] != "":
        orderBy = kwargs['orderBy']
    else:
        orderBy = kwargs['defaultOrderBy']
    return {'activePage' : currentPage, 'orderBy' : orderBy }
