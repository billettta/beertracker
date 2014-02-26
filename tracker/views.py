from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from tracker.models import Beer,Rating,RatingForm

def index(request):
    return HttpResponse("hello world")

def beerDetail(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    #should limit for 10 or so with pagination
    ratings = Rating.objects.filter(beer=beer_id)
    form = RatingForm()
    return render(request, 'tracker/beerDetail.html',{'beer':beer,'rating_list':ratings,'form':form})

def breweryDetail(request, brewery_id):
    brewery = get_object_or_404(Brewery, pk=brewery_id)
    #should limit for 10 or so with pagination
    beers = Beer.objects.filter(brewery=brewery_id)
    return render(request, 'tracker/breweryDetail.html',{'brewery',brewery})

def ratingDetail(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    return render(request, 'tracker/ratingDetail.html',{'rating',rating})

def styleDetail(request, style_id):
    style = get_object_or_404(Beer, pk=style_id)
    return render(request, 'tracker/styleDetail.html',{'style',style})

def myRatings(request,tracker_id):
    #should probably actually look up on logged in user
    ratings  = Ratigns.objects.filter(tracker=tracker_id)
    return render(request, 'tracker/ratingsList.html',{'ratings',ratings})

#do we actually need a style list view ?
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

def advocate(request):
    return render_to_response('tracker/advocate.html')
