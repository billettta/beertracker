from django.contrib import admin
from tracker.models import Beer 
from tracker.models import Brewery 
from tracker.models import Style 
from tracker.models import Taster 
from tracker.models import Rating 

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(Style)
admin.site.register(Taster)
admin.site.register(Rating)

# Register your models here.
