from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from tracker.models import Beer,Rating,RatingForm,NewUserForm,Brewery,Style,NewTasterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Count
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import FieldError
from django.contrib import messages 
import sys

def index(request):
    beerCount = Beer.objects.count()
    breweryCount = Brewery.objects.count()
    ratingCount = Rating.objects.count()
    return render(request, 'tracker/welcome.html',{'beerCount':beerCount,'breweryCount':breweryCount,'ratingCount':ratingCount}, context_instance=RequestContext(request))

def search(request, searchString):
    orderByField = request.GET.get('order_by', 'name')
    panelID = request.GET.get('panelID', 'all')

    if(len(searchString) < 3):
        messages.warning(request,'Search string must be at least three characters')
        return render(request, 'tracker/searchResults.html', context_instance=RequestContext(request))

    beers = None
    breweries = None
    styles = None
    
    if panelID == 'beerPanel' or panelID == 'all':
        beer_list = Beer.objects.filter(name__icontains=searchString).annotate(avg_rating=Avg('rating__overallRating'), avg_volume=Avg('rating__volumeRating')).order_by(orderByField)
        paginator = Paginator(beer_list, 20) #Show 20 beers per page
        page = request.GET.get('page')
        try:
            beers = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            beers = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            beers = paginator.page(paginator.num_pages) 

    if panelID == 'breweryPanel' or panelID == 'all':
        brewery_list = Brewery.objects.filter(name__icontains=searchString).annotate(beer_count=Count('beer')).order_by(orderByField)
        paginator2 = Paginator(brewery_list, 20) #Show 20 beers per page
        page2 = request.GET.get('page')
        try:
            breweries = paginator2.page(page2)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            breweries = paginator2.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            breweries = paginator2.page(paginator2.num_pages) 

    if panelID == 'stylePanel' or panelID == 'all':
        style_list=Style.objects.filter(name__icontains=searchString).annotate(beer_count=Count('beer')).order_by(orderByField)
        paginator3 = Paginator(style_list, 20) #Show 20 beers per page
        page3 = request.GET.get('page')
        try:
            styles = paginator3.page(page3)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            styles = paginator3.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            styles = paginator3.page(paginator3.num_pages) 

    if request.is_ajax():
        if panelID == 'beerPanel':
            template = 'tracker/beerTable.html'
        elif panelID == 'breweryPanel':
            template = 'tracker/breweryTable.html'
        elif panelID == 'stylePanel':
            template = 'tracker/styleTable.html'
    else:
        template = 'tracker/searchResults.html'

    return render(request, template, {'beers':beers,'breweries':breweries,'styles':styles}, context_instance=RequestContext(request))

def beerDetail(request, beer_id):
    beer = None
    form = None

    if request.is_ajax():
        template = 'tracker/beerRatingTable.html'
    else:
        template = 'tracker/beerDetail.html'
        beer = get_object_or_404(Beer, pk=beer_id)
        if request.method == 'POST':
            rf = RatingForm(request.POST, request.FILES)
            if rf.is_valid():
                ratingForm = rf.save(commit=False)
                ratingForm.user = request.user
                ratingForm.beer = beer
                ratingForm.save()
                messages.success(request, 'Rating submitted successfully!')
            else:
                form = rf
        
        beer = get_object_or_404(Beer.objects.all().annotate(avg_rating=Avg('rating__overallRating'), avg_volume=Avg('rating__volumeRating')), pk=beer_id)
        form = RatingForm()
    
    orderByField = request.GET.get('order_by', '-date')
    if request.user.is_authenticated():
        rating_list = Rating.objects.filter(beer=beer_id).extra(select={'userOrder': '''CASE WHEN user_id = ''' + str(request.user.id) + ''' THEN 0 ELSE 1 END'''}).extra(order_by=['userOrder', orderByField, '-id'])
    else:
        rating_list = Rating.objects.filter(beer=beer_id).order_by(orderByField,'-id')

    paginator = Paginator(rating_list, 10) #Show 10 ratings per page
    page = request.GET.get('page')
    try:
        ratings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ratings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ratings = paginator.page(paginator.num_pages)



    return render(request, template, {'beer':beer,'rating_list':ratings,'form':form}, context_instance=RequestContext(request))

def breweryDetail(request, brewery_id):
    brewery = get_object_or_404(Brewery, pk=brewery_id)
    orderByField = request.GET.get('order_by', 'name')
    beer_list = Beer.objects.filter(brewery=brewery_id).annotate(avg_rating=Avg('rating__overallRating'), avg_volume=Avg('rating__volumeRating')).order_by(orderByField)
    paginator = Paginator(beer_list, 20) #Show 20 beers per page
    page = request.GET.get('page')
    try:
        beers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        beers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        beers = paginator.page(paginator.num_pages)

    if request.is_ajax():
        template = 'tracker/beerTable.html'
    else:
        template = 'tracker/breweryDetail.html'

    return render(request, template,{'brewery':brewery,'beers':beers }, context_instance=RequestContext(request))

def ratingDetail(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    return render(request, 'tracker/ratingDetail.html',{'rating',rating})

def styleDetail(request, style_id):
    style = None
    if request.is_ajax():
        template = 'tracker/beerTable.html'
    else:
        template = 'tracker/styleDetail.html'
        style = get_object_or_404(Style, pk=style_id)

    orderByField = request.GET.get('order_by', 'name')
    beer_list = Beer.objects.filter(style=style_id).annotate(avg_rating=Avg('rating__overallRating'), avg_volume=Avg('rating__volumeRating')).order_by(orderByField)
    paginator = Paginator(beer_list, 20) #Show 20 beers per page
    page = request.GET.get('page')
    try:
        beers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        beers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        beers = paginator.page(paginator.num_pages)
    return render(request, template, {'style':style, 'beers':beers}, context_instance=RequestContext(request))

@login_required(login_url='/tracker/login/')
def myProfile(request):
    return redirect(profile, request.user.id )

def profile(request, user_id):
    user = None
    if request.is_ajax():
        template = 'tracker/userRatingTable.html'
    else:
        template = 'tracker/profile.html'
        user = get_object_or_404(User, pk=user_id)

    orderByField = request.GET.get('order_by', '-date')
    rating_list = Rating.objects.filter(user_id=user_id).order_by(orderByField)
    paginator = Paginator(rating_list, 10) #Show 10 ratings per page
    page = request.GET.get('page')
    try:
        ratings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ratings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ratings = paginator.page(paginator.num_pages)

    return render(request, template, { 'userProfile': user, 'rating_list':ratings }, context_instance=RequestContext(request))


#do we actually need a style list view ?
#maybe as a way to select a style and then view all of the beers of it
def styleList(request):
    orderByField = request.GET.get('order_by', 'name')
    style_list = Style.objects.all().annotate(beer_count=Count('beer')).order_by(orderByField)
    paginator = Paginator(style_list, 20) #Show 20 styles per page
    page = request.GET.get('page')
    try:
        styles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        styles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        styles = paginator.page(paginator.num_pages)

    if request.is_ajax():
        template = 'tracker/styleTable.html'
    else:
        template = 'tracker/styleList.html'

    return render(request, template, {'styles':styles }, context_instance=RequestContext(request))

def breweryList(request):
    orderByField = request.GET.get('order_by', 'name')
    brewery_list = Brewery.objects.all().annotate(beer_count=Count('beer')).order_by(orderByField)
    paginator = Paginator(brewery_list, 20) #Show 20 breweries per page
    page = request.GET.get('page')
    try:
        breweries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        breweries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        breweries = paginator.page(paginator.num_pages)

    if request.is_ajax():
        template = 'tracker/breweryTable.html'
    else:
        template = 'tracker/breweryList.html'

    return render(request, template, {'breweries':breweries }, context_instance=RequestContext(request))

def ratingList(request):
    return HttpResponse("You're looking at beer %s.")

def beerList(request):
    orderByField = request.GET.get('order_by', 'name')
    beer_list = Beer.objects.all().annotate(avg_rating=Avg('rating__overallRating'), avg_volume=Avg('rating__volumeRating')).order_by(orderByField)
    paginator = Paginator(beer_list, 20) #Show 20 beers per page
    page = request.GET.get('page')
    try:
        beers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        beers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        beers = paginator.page(paginator.num_pages)

    if request.is_ajax():
        template = 'tracker/beerTable.html'
    else:
        template = 'tracker/beerList.html'

    return render(request, template, {'beers':beers }, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser, login_url='/tracker/login/')
def advocate(request):
    return render_to_response('tracker/advocate.html')

def register(request):    
    if request.method == 'POST':
        uf = NewUserForm(request.POST)
        tf = NewTasterForm(request.POST, request.FILES)
        if uf.is_valid() and tf.is_valid():
            try:
                user = uf.save()
                taster = tf.save(commit=False)
                taster.user = user
                taster.save()
                new_user = authenticate(username=request.POST['username'],
                                        password=request.POST['password'])
                login(request, new_user)
                return redirect(request.GET.get('next', '/tracker/profile/'))
            except Exception, e:
                User.objects.filter(id=user.id).delete()
                messages.warning(request, "Exception occured: " + str(e))
                return render(request, 'tracker/register.html', { 'form': uf, 'tasterForm': tf } )
        else:
            return render(request, 'tracker/register.html', { 'form': uf, 'tasterForm': tf } )
    else:
        form = NewUserForm();
        tasterForm = NewTasterForm();
        return render(request, 'tracker/register.html', { 'form': form, 'tasterForm': tasterForm } )

def logout_page(request):
    logout(request)
    return redirect(request.GET.get('next', '/tracker/'))




