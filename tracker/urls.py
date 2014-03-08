from django.conf.urls import patterns,url
from tracker import views


urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),

    url(r'^register/?$',views.register,name='register'),
    url(r'^login/?$','django.contrib.auth.views.login', {'template_name': 'tracker/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',  {'login_url':'/tracker/login/'}),
    url(r'^beer/(?P<beer_id>\d+)/?$', views.beerDetail, name='beerDetail'),
    url(r'^brewery/(?P<brewery_id>\d+)/?$', views.breweryDetail, name='breweryDetail'),
    url(r'^style/(?P<style_id>\d+)/?$', views.styleDetail, name='styleDetail'),
    url(r'^profile/?$', views.myProfile, name='myProfile'),
    url(r'^profile/(?P<user_id>\d+)/?$', views.profile, name='profile'),
    url(r'^(?P<poll_id>\d+)/$', views.beerDetail, name='beerDetail'),
    url(r'^(?P<beer_id>\d+)/beer/$', views.beerDetail, name='beerDetail'),
)
