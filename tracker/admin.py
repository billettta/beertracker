from django.contrib import admin
from tracker.models import Beer, Brewery, Style, Taster, Rating 

admin.site.register(Beer, Brewery, Style, Taster, Rating)

# Register your models here.
