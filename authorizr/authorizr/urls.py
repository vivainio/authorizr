from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from allauth.account.views import logout
#from allauth.socialaccount.views import login_cancelled, login_error
#from allauth.facebook.views import login as facebook_login


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'authorizr.views.home', name='home'),
    # url(r'^authorizr/', include('authorizr.foo.urls')),
    url("^appreg/$", "appreg.views.index"),
    url("^appreg/myapps/", "appreg.views.myapps"),
    #url(r'^accounts/', include('allauth.urls')),
    url(r'^login/google/', 'appreg.views.googlelogin'),
    url(r'^login/startlogin/', 'appreg.views.startlogin'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
