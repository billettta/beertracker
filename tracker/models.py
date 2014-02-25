from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Brewery(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField()
    def __unicode__(self):
        return self.name
#    flagship = models.ForeignKey(Beer)

class Style(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lowabv = models.DecimalField(max_digits=3,decimal_places=1)
    highabv = models.DecimalField(max_digits=3,decimal_places=1)
    def __unicode__(self):
        return self.name

class Beer(models.Model):
    brewery = models.ForeignKey(Brewery)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    style = models.ForeignKey(Style)
    abv = models.DecimalField(max_digits=3,decimal_places=1)
    #uploads to MEDIA_ROOT/beershots need to serve from apache or S3(eventually)
    #need to figure out how to rename to name of beer and put in folder for brewery
    picture = models.ImageField(upload_to='beershots')
    # additional fields: average rating ?
    def __unicode__(self):
        return self.name

class Taster(models.Model):
#    user = models.OneToOneField(User)
    description = models.TextField(blank=True)
    nickName = models.CharField(max_length=250,blank=True)
    # think these might be able to be pulled in from generic user class
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    def __unicode__(self):
        return self.nickName

class Rating(models.Model):
    beer = models.ForeignKey(Beer)
    taster = models.ForeignKey(Taster)
    date = models.DateField()
    overallRating = models.DecimalField(max_digits=3,decimal_places=1)
    volumeRating = models.DecimalField(max_digits=3,decimal_places=1,blank=True)
    notes = models.TextField(blank=True)
    # right now this is calculated when called instead of stored in DB probably want to switch so its only calculated once
    def _get_drunk(self):
        "Returns the drunkability"
        return (beer.abv * self.VolumeRating)/10
    drunkRating = property(_get_drunk)

class Quote(models.Model):
    authors = models.ManyToManyField(Taster)
    quoteText = models.TextField()
    #should be taken from logged in user
#    submiter = models.ForeignKey(Taster)

#additional objects: team ?
