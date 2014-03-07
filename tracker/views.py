from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from tracker.models import Beer,Rating,RatingForm,NewUserForm,Brewery,Style
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max

def index(request):
    return HttpResponse("hello world")

def beerDetail(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    form = RatingForm()

    if request.method == 'POST':
        rf = RatingForm(request.POST, request.FILES)
        if rf.is_valid():
            ratingForm = rf.save(commit=False)
            ratingForm.user = request.user
            ratingForm.beer = beer
            ratingForm.save()
        else:
            form = rf

    orderByField = request.GET.get('order_by', '-date')
    rating_list = Rating.objects.filter(beer=beer_id).order_by(orderByField)
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


    return render(request, 'tracker/beerDetail.html',{'beer':beer,'rating_list':ratings,'form':form}, context_instance=RequestContext(request))

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
    return render(request, 'tracker/breweryDetail.html',{'brewery':brewery,'beers':beers }, context_instance=RequestContext(request))

def ratingDetail(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    return render(request, 'tracker/ratingDetail.html',{'rating',rating})

def styleDetail(request, style_id):
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
    return render(request, 'tracker/styleDetail.html',{'style':style, 'beers':beers}, context_instance=RequestContext(request))

#this could maybe be a on a profile page instead ?
def myRatings(request,tracker_id):
    #should probably actually look up on logged in user
    ratings  = Ratigns.objects.filter(tracker=tracker_id)
    return render(request, 'tracker/ratingsList.html',{'ratings',ratings})

#do we actually need a style list view ?
#maybe as a way to select a style and then view all of the beers of it
def styleList(request):
    return HttpResponse("You're looking at beer %s.")

#def beerList(request):
   # latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
   # context = {'latest_poll_list': latest_poll_list}
#    return render(request, 'tracker/index.html', context)

def breweryList(request):
    return HttpResponse("You're looking at beer %s.")

def ratingList(request):
    return HttpResponse("You're looking at beer %s.")


@login_required(login_url='/tracker/login/')
def advocate(request):
    return render_to_response('tracker/advocate.html')

def register(request):    
    if request.method == 'POST':
        uf = NewUserForm(request.POST)
        if uf.is_valid():
            user = uf.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return redirect(index)   
        else:
            return render(request, 'tracker/register.html', { 'form': uf } )
    else:
        form = NewUserForm();
        return render(request, 'tracker/register.html', { 'form': form } )





