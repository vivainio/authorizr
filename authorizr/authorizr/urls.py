from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

import appreg.views

import userreg.views

import subreg.views

from django.contrib.auth.decorators import login_required


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
 
    url("^appreg/myapps/", login_required(appreg.views.AppListView.as_view())),
    url("^appreg/editapp/(?P<appuid>\w{1,255})/$", "appreg.views.edit_app_credentials"),
    url("^appreg/deleteapp/(?P<appuid>\w{1,255})/$", "appreg.views.delete_application"),
    url("^appreg/addapp/", "appreg.views.add_application"),
            
    #Google Login 
    url("^userreg/login/", "userreg.views.create_google_session"),
    url("^userreg/userlogincallback/", "userreg.views.google_profile_callback"),
            
    #Authentication    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'appreg.views.logout_view'),
    url(r'^login/startlogin/', 'appreg.views.startlogin'),    
    
    #After login, user is redirected to profile. Let's make it to point front page
    url(r'^accounts/profile/$', 'appreg.views.frontpage'), 
        
    #REST API URLs
    url(r'^login/oauth2callback/', 'restapi.views.login_callback'),
    url(r'^api/v1/create_session/(?P<appid>\w{1,255})/$', 'restapi.views.create_session'),
    url(r'^api/v1/fetch_access_token/(?P<sessionid>\w{1,255})/$', 'restapi.views.fetch_access_token'),
    url(r'^api/v1/refresh_access_token/(?P<appid>\w{1,255})/$', 'restapi.views.refresh_access_token'),

    # subscription api

    url(r'^api/sub/v1/consume/res/(?P<resourceid>\w{1,255})/$', 'subapi.views.consume'),

    url(r'^subreg/resources/',subreg.views.ResourcesListView.as_view()),
    url(r'^subreg/addresource/', "subreg.views.add_resource"),
    url(r'^subreg/editres/(?P<resid>\w{1,255})/$', 'subreg.views.edit_resource'),
    url(r'^subreg/deleteres/(?P<resid>\w{1,255})/$', 'subreg.views.delete_resource'),
    url(r'^subreg/subscriptions/(?P<resid>\w{1,255})/$', 'subreg.views.subsforresource'),
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()