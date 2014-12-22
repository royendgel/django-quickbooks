from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^$', 'server.views.home'),
    url(r'^wsdl$', 'server.views.show_wsdl'),
)
