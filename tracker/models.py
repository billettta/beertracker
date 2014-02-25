from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Brewery(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField()
    def __unicode__(self):
        return self.name
#    flagship = models.ForeignKey(Beer)

class Style(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lowabv = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    highabv = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    def __unicode__(self):
        return self.name

class Beer(models.Model):
    brewery = models.ForeignKey(Brewery)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    style = models.ForeignKey(Style)
    abv = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    #uploads to MEDIA_ROOT/beershots need to serve from apache or S3(eventually)
    #need to figure out how to rename to name of beer and put in folder for brewery
    picture = models.ImageField(upload_to='beershots')
    retired = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Taster(models.Model):
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)
    nickName = models.CharField(max_length=250,blank=True)
    email = models.EmailField(max_length=254)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.nickName

class Rating(models.Model):
    beer = models.ForeignKey(Beer)
    taster = models.ForeignKey(Taster)
    date = models.DateField()
    overallRating = models.DecimalField(max_digits=3,decimal_places=1)
    volumeRating = models.DecimalField(max_digits=3,decimal_places=1,blank=True)
    notes = models.TextField(blank=True)
    def _get_drunk(self):
        "Returns the drunkability"
        return (beer.abv * self.VolumeRating)/10
    drunkRating = property(_get_drunk)

