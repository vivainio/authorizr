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
    url("^$", "appreg.views.frontpage"),
    url("^appreg/$", "appreg.views.frontpage"),
    url("^appreg/myapps/", "appreg.views.myapps"),
    #url(r'^accounts/', include('allauth.urls')),
    url(r'^login/google/', 'appreg.views.googlelogin'),
    url(r'^login/startlogin/', 'appreg.views.startlogin'),
    
    #Authentication    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'appreg.views.logout_view'),
    
    #After login, user is redirected to profile. Let's make it to point fron page
    url(r'^accounts/profile/$', 'appreg.views.frontpage'), 
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
