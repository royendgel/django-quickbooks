from django.conf.urls import patterns, include, url

from quickbooks.views import GetQWCFileView

urlpatterns = patterns('',
    url(r'^$', 'quickbooks.views.home'),
    url(r'^wsdl$', 'quickbooks.views.show_wsdl'),
    url(r'^get-company-file', GetQWCFileView.as_view()),
)
