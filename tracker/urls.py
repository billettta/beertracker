from django.conf.urls import patterns,url
from tracker import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^beer/(?P<beer_id>\d+)/$', views.beerDetail, name='beerDetail'),
    url(r'^(?P<poll_id>\d+)/$', views.beerDetail, name='beerDetail'),
    url(r'^(?P<beer_id>\d+)/beer/$', views.beerDetail, name='beerDetail'),
)
