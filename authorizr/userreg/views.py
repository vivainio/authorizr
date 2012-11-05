

import uuid

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render

from restapi.sanction.client import Client

from django.contrib import auth
from django.contrib.auth import authenticate, login
from userreg.models import OIConnectUser 

from appreg.models import AppCredentials, AuthSession

import json 
from urlparse import parse_qsl

from django.conf import settings


def make_google_client():
        
    client = Client(
        auth_endpoint = "https://accounts.google.com/o/oauth2/auth",
        token_endpoint= "https://accounts.google.com/o/oauth2/token",
        resource_endpoint = "https://www.googleapis.com/oauth2/v1",
        client_id = settings._CLIENT_ID,
        client_secret = settings._CLIENT_SECRET,
        redirect_uri = settings._REDIRECT_URI
        )
    
    return client

def google_oi_connect_login(request):
         
    args = dict(request.REQUEST.iteritems())
    #cred_id = args['cred_id']        
      
    client = make_google_client()
    
    uid = uuid.uuid4().hex
    url = client.auth_uri({'https://www.googleapis.com/auth/userinfo.profile',
                           'https://www.googleapis.com/auth/userinfo.email',}, state = uid)
    
    # get authorization
    return HttpResponseRedirect(url)
    
def google_oi_connect_login_callback(request):
    
    client = make_google_client()
    
    
    rdict = request.REQUEST
    print "requesting token"
    print "State",rdict['state']
    d = {'code' : rdict["code"]}
    
    def tries_parser(s):
        try:
            val = json.loads(s)
        except ValueError:
            val = dict(parse_qsl(s))
        #print "Parsed",val
        return val
    
    client.request_token(tries_parser, **d)
    
    # if all goes well in previous call
    userinfo = client.request("/userinfo")
    print userinfo    
    
    user = authenticate(user_info=userinfo)
    
    if user is not None:
        login(request, user)
    else:
        #store data to session, user is only created if adding is confirmed
        request.session['userinfo'] = userinfo 
        return render(request, 'userreg/confirm.html', {'info': userinfo})
    
    return HttpResponseRedirect("/")   
   
    
def confirm_and_make_user(request):
        
        userinfo = request.session.get('userinfo', None)
        print "session userinfo"
        
        print userinfo
        
        new_user = OIConnectUser.objects.create(
                                            user_id = userinfo["id"], 
                                            username = userinfo["email"],
                                            email = userinfo["email"],
                                            first_name = userinfo.get("given_name", " "),
                                            last_name = userinfo.get("family_name", " "),
                                            is_active = True,
                                            is_staff = False,
                                            password = uuid.uuid4().hex)
                                            
        new_user.save()        
        print "user created"
        
        user = authenticate(user_info=userinfo)

        if user is not None:
            print "new user found"
            login(request, user)
            
        return HttpResponseRedirect("/")
    

       