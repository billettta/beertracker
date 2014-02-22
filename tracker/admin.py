from django.contrib import admin
from tracker.models import Beer, Brewery, Style, Taster, Rating 

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(Style)
admin.site.register(Rating)
admin.site.register(Taster)

# Register your models here.
