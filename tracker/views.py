from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from tracker.models import Beer,Rating,RatingForm,NewUserForm,Brewery,Style
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Count
from django.contrib.auth.decorators import user_passes_test

def index(request):
    beerCount = Beer.objects.count()
    breweryCount = Brewery.objects.count()
    ratingCount = Rating.objects.count()
    return render(request, 'tracker/welcome.html',{'beerCount':beerCount,'breweryCount':breweryCount,'ratingCount':ratingCount}, context_instance=RequestContext(request))

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

@login_required(login_url='/tracker/login/')
def myProfile(request):
    return redirect(profile, request.user.id )

def profile(request, user_id):
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


    return render(request, 'tracker/profile.html',{ 'userProfile': user, 'rating_list':ratings }, context_instance=RequestContext(request))


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
    return render(request, 'tracker/styleList.html',{'styles':styles }, context_instance=RequestContext(request))

#def beerList(request):
   # latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
   # context = {'latest_poll_list': latest_poll_list}
#    return render(request, 'tracker/index.html', context)

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
    return render(request, 'tracker/breweryList.html',{'breweries':breweries }, context_instance=RequestContext(request))

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
    return render(request, 'tracker/beerList.html',{'beers':beers }, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser, login_url='/tracker/login/')
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
            return redirect(request.GET.get('next', '/tracker/profile/'))
        else:
            return render(request, 'tracker/register.html', { 'form': uf } )
    else:
        form = NewUserForm();
        return render(request, 'tracker/register.html', { 'form': form } )

def logout_page(request):
    logout(request)
    return redirect(request.GET.get('next', '/tracker/'))




