from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^$', 'quickbooks.views.home'),
    url(r'^wsdl$', 'quickbooks.views.show_wsdl'),
    url(r'^get-company-file', 'quickbooks.views.get_company_file'),
)
