from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from captive_portal import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fwpubwifi01.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home),
    url(r'^splash$', views.splash, name='splash'),
    url(r'^splash_action$', views.splash_action, name='splash_action'),
)

