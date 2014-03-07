from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

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
    picture = models.ImageField(upload_to='beershots',blank=True)
    # additional fields: average rating ?
    retired = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

#do we even need this class ? description is the only one that would be covered in the generic user
class Taster(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(blank=True)
    nickName = models.CharField(max_length=250,blank=True)
    picture = models.ImageField(upload_to='tastershots',blank=True)
    def __unicode__(self):
        return self.nickName

class Rating(models.Model):
    beer = models.ForeignKey(Beer)
    user = models.ForeignKey(User)
    date = models.DateField()
    overallRating = models.DecimalField(max_digits=3,decimal_places=1)
    volumeRating = models.DecimalField(max_digits=3,decimal_places=1,blank=True)
    notes = models.TextField(blank=True)
    picture = models.ImageField(upload_to='ratingshots',blank=True)
    # right now this is calculated when called instead of stored in DB probably want to switch so its only calculated once
    def _get_drunk(self):
        "Returns the drunkability"
        return (beer.abv * self.VolumeRating)/10
    drunkRating = property(_get_drunk)

class Quote(models.Model):
    authors = models.ManyToManyField(User)
    quoteText = models.TextField()
    #should be taken from logged in user
#    submiter = models.ForeignKey(Taster)

class RatingForm(ModelForm):
    class Meta:
        model = Rating 
        fields = ['date', 'overallRating','volumeRating','notes','picture']

class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

#additional objects: team ?
