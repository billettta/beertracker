from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
import datetime

#TODO: limit image sizes
#TODO: uploads to media need to serve from apache or S3(eventually)
#TODO: rename files on upload to avoid duplicate filenames
#TODO: calculate ratings andn drunkability on insert instead of on every read


class Brewery(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField()
    def __unicode__(self):
        return self.name

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
    picture = models.ImageField(upload_to='beershots',blank=True)
    retired = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=250,blank=True)
    picture = models.ImageField(upload_to='teamshots',blank=True)
    description = models.TextField(blank=True)

class Taster(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to='tastershots',blank=True)
    team = models.ForeignKey(Team,blank=True,null=True)
    nickName = models.CharField(max_length=250,blank=True)
    def __unicode__(self):
        return self.nickName

class Event(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()
    team = models.ForeignKey(Team,blank=True,null=True)

class Rating(Event):
    beer = models.ForeignKey(Beer)
    overallRating = models.DecimalField(max_digits=3,decimal_places=1)
    volumeRating = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    drunkRating = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    notes = models.TextField(blank=True)
    picture = models.ImageField(upload_to='ratingshots',blank=True)

class Quote(Event):
    authors = models.ManyToManyField(User,related_name="author")
    quoteText = models.TextField()


class Picture(Event):
    picture = models.ImageField(upload_to='shots',blank=True)
    caption = models.CharField(max_length=250,blank=True)

class TeamForm(ModelForm)
    class Meta:
        model = Team
        fields = ['name','picture','description']

class RatingForm(ModelForm):
    date = forms.DateTimeField(input_formats=['%m/%d/%Y'],initial=datetime.date.today().strftime("%d/%m/%Y"))
    overallRating = forms.DecimalField(max_digits=3,decimal_places=1,min_value=0,max_value=10.0,required=True)
    volumeRating = forms.DecimalField(max_digits=3,decimal_places=1,min_value=0,max_value=10.0,required=False)
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

class NewTasterForm(ModelForm):
    class Meta:
        model = Taster
        fields = ['nickName', 'description', 'picture']
        
