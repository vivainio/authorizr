

import uuid

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render

from restapi.sanction.client import Client

from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login

from appreg.models import AppCredentials, AuthSession

import json 
from urlparse import parse_qsl


def make_google_client():
    client = Client(
        auth_endpoint = "https://accounts.google.com/o/oauth2/auth",
        token_endpoint= "https://accounts.google.com/o/oauth2/token",
        resource_endpoint = "https://www.googleapis.com/oauth2/v1",
        client_id = "172254031599.apps.googleusercontent.com",
        client_secret = "UuJfm-vgRxTNdfxxZFPcydy8",
        redirect_uri = "http://127.0.0.1:8000/userreg/userlogincallback"
        )
    return client

def create_google_session(request):
         
    args = dict(request.REQUEST.iteritems())
    #cred_id = args['cred_id']        
      
    client = make_google_client()
    
    uid = uuid.uuid4().hex
    url = client.auth_uri({'https://www.googleapis.com/auth/userinfo.profile',
                           'https://www.googleapis.com/auth/userinfo.email',}, state = uid)
    
    # get authorization
    return HttpResponseRedirect(url)
    
def google_profile_callback(request):
    
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
    info = client.request("/userinfo")
    print info    
    
    user = check_user(info)

    print user.is_active
    
    if user.is_active:  
        user.backend = 'django.contrib.auth.backends.ModelBackend'    
        login(request, user)

    
    return HttpResponseRedirect("/")   

def check_user(google_user):
    
    try:        
        u = User.objects.get(email = google_user["email"])
        print "user exists"       
        return u
    except User.DoesNotExist:
        print "user does not exist"
        return make_user(google_user)
    
    
    
    
def make_user(google_user):
        user = User.objects.create_user(google_user["name"], google_user["email"], uuid.uuid4().hex )
        user.is_staff = False
        
        print "user created "
        print user
        user.save()
        return user
        
       