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
 
    #url("^appreg/myapps/", login_required(appreg.views.AppListView.as_view())),
    url("^appreg/myapps/", "appreg.views.myapps"),

    url("^appreg/editapp/(?P<appuid>\w{1,255})/$", "appreg.views.edit_app_credentials"),
    url("^appreg/deleteapp/(?P<appuid>\w{1,255})/$", "appreg.views.delete_application"),
    url("^appreg/addapp/", "appreg.views.add_application"),
            
    #Google OpenId Connect login 
    url("^userreg/login/", "userreg.views.google_oi_connect_login"),
    url("^userreg/userlogincallback/", "userreg.views.google_oi_connect_login_callback"),
    url("^userreg/confirm/", "userreg.views.confirm_and_make_user"),            
    #Authentication    
    url(r'^accounts/login/$', 'appreg.views.login'),
    url(r'^accounts/logout/$', 'appreg.views.logout_view'),
    #url(r'^login/startlogin/', 'appreg.views.startlogin'),    
    
    #After login, user is redirected to profile. Let's make it to point front page
    url(r'^accounts/profile/$', 'appreg.views.frontpage'), 
        
    # OAuth2


    #insp: change to api/oauth2/v1/oauth2callback
    url(r'^login/oauth2callback/', 'restapi.views.login_callback'),
    
    # insp: change to api/oauth2/v1/create_session etc
    url(r'^api/v1/create_session/(?P<appid>\w{1,255})/$', 'restapi.views.create_session'),
    url(r'^api/v1/fetch_access_token/(?P<sessionid>\w{1,255})/$', 'restapi.views.fetch_access_token'),
    url(r'^api/v1/refresh_access_token/(?P<credential_uid>\w{1,255})/$', 'restapi.views.refresh_access_token'),
    url(r'^api/v1/maintenance/(?P<period>\w{1,255})/$', 'restapi.views.run_maintenance'),

    # subscription api

    url(r'^api/sub/v1/consume/res/(?P<resourceid>[\w\.]{1,255})$', 'subapi.views.consume'),

    url(r'^subreg/resources/',login_required(subreg.views.ResourcesListView.as_view())),
    url(r'^subreg/addresource/', "subreg.views.add_resource"),
    url(r'^subreg/editres/(?P<resid>\w{1,255})/$', 'subreg.views.edit_resource'),
    url(r'^subreg/deleteres/(?P<resid>\w{1,255})/$', 'subreg.views.delete_resource'),
    url(r'^subreg/subscriptions/(?P<resid>\w{1,255})/$', 'subreg.views.subsforresource'),
    
    # OAuth1
    
    url(r'^dump', 'oauth1api.views.dump_request'),
    url(r'^api/oauth1/v1/create_session/(?P<appid>\w{1,255})/$', 'oauth1api.views.create_session'),
    
    # insp: change to api/oauth1/v1/oauth1callback
    url(r'^login/v1/oauth1callback', 'oauth1api.views.login_callback'),
    url(r'^api/oauth1/v1/fetch_access_token/(?P<sessionid>\w{1,255})/$', 'oauth1api.views.fetch_access_token'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()