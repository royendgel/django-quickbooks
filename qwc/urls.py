from django.conf.urls import patterns, include, url

from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'quickbooks.views.welcome'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^quickbooks/', include('quickbooks.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
