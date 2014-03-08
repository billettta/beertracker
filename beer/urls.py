from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'beer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tracker/', include('tracker.urls')),
    url(r'^advocate/$', 'tracker.views.advocate'),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/apps/static'}),
)#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
