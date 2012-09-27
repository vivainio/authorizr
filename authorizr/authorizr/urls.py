from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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
    url("^$", "appreg.views.frontpage"),
    url("^appreg/$", "appreg.views.frontpage"),
    url("^appreg/myapps/", "appreg.views.myapps"),
    url("^appreg/editapp/(?P<appuid>\w{1,255})/$", "appreg.views.editapp"),
    url("^appreg/editapp/(?P<appuid>\d{1,255})/update/$", "appreg.views.updateapp"),

    #url(r'^accounts/', include('allauth.urls')),
    
    #Authentication    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'appreg.views.logout_view'),
    url(r'^login/startlogin/', 'appreg.views.startlogin'),    
    
    #After login, user is redirected to profile. Let's make it to point front page
    url(r'^accounts/profile/$', 'appreg.views.frontpage'), 
        
    #REST API URLs
    url(r'^login/google/', 'restapi.views.login_callback'),
    url(r'^api/v1/create_session/', 'restapi.views.create_session'),
    url(r'^api/v1/fetch_access_token/', 'restapi.views.fetch_access_token'),
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()