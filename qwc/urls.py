from django.conf.urls import patterns, include, url

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'quickbooks.views.welcome'),
    url(r'^quickbooks/', include('quickbooks.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
