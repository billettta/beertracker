from django.conf.urls import patterns,url
from tracker import views


urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),

    url(r'^register/?$',views.register,name='register'),
    url(r'^login/?$','django.contrib.auth.views.login', {'template_name': 'tracker/login.html'}),
    url(r'^logout/?$', views.logout_page, name='logout_page'),
    url(r'^search/(?P<searchString>\w*)/?$', views.search, name='search'),
    url(r'^beer/(?P<beer_id>\d+)/?$', views.beerDetail, name='beerDetail'),
    url(r'^brewery/(?P<brewery_id>\d+)/?$', views.breweryDetail, name='breweryDetail'),
    url(r'^style/(?P<style_id>\d+)/?$', views.styleDetail, name='styleDetail'),
    url(r'^profile/?$', views.myProfile, name='myProfile'),
    url(r'^profile/(?P<user_id>\d+)/?$', views.profile, name='profile'),
    url(r'^beers/?$', views.beerList, name='beerList'),
    url(r'^breweries/?$', views.breweryList, name='breweryList'),
    url(r'^styles/?$', views.styleList, name='styleList'),
)
