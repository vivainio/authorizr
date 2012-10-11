
import urllib
import uuid

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render


from sanction.client import Client

from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required

from appreg.models import AppCredentials, AuthSession

import json 
from urlparse import parse_qsl
from httplib2 import Credentials


def make_client(credentials):
    c = Client(
        auth_endpoint = credentials.auth_endpoint,
        token_endpoint = credentials.token_endpoint,
        resource_endpoint = credentials.resource_endpoint,
        client_id = credentials.app_api_key,
        client_secret = credentials.app_secret,
        redirect_uri = credentials.redirect_uri)        
    return c
    

def make_auth_session(cred, uid):
    authSession = AuthSession(
                    session_id = uid,
                    access_token = '',
                    refresh_token = '',
                    credentials = cred,
                    )
    
    authSession.save()
    return authSession
    
    
def create_session(request, appid):
     
    credential_uid = appid
    
    print "creating session for: "+credential_uid
    
    args = dict(request.REQUEST.iteritems())
        
    try:       
        credentials = AppCredentials.objects.get(uid=credential_uid)
    except AppCredentials.DoesNotExist:
        return HttpResponse(content="Application for specified handle not found", status=404)
       
    #Make unique ID for request    
    uid = uuid.uuid4().hex
    
    #initiate db entry for this session
    auth_session = make_auth_session(credentials, uid)
    
    scope = tuple(args.get('scope', credentials.scope).split(" "))    
    
    #Initialize sanction client
    c = make_client(credentials)    
            
    #custom parameters so that we can get refresh_token
    #google calls this offline access
    
    ##params = {'access_type': 'offline',
    ##          'approval_prompt':'force'}
        
    #Construct authentication URI using Sanction
    url = c.auth_uri(scope, state = uid,**args)
      
    json_response = json.dumps({"session_id": uid, "url": url})
    
    return HttpResponse(json_response, "application/json")
        
        
def login_callback(request):
    
    print "LOGIN_CALLBACK"
        
    sid = request.REQUEST['state']
    
    print "SID: "+ sid
    
    try:       
        a = AuthSession.objects.get(session_id = sid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    print "a.credentials.app_dec"
    print a.credentials.app_desc    
            
    c = make_client(a.credentials)    
        
    rdict = request.REQUEST
    print "REQUEST:"
    print rdict
        
    d = {'code' : rdict["code"]}
       
    c.request_token(token_response_parser, **d)
    
    print "token received!"
    print c.access_token
             
    a.access_token = c.access_token;
    
        
    try:
        print "refresh token received!: "+ c.refresh_token
        a.refresh_token = c.refresh_token
    except AttributeError:
        print "no refresh token here"
            
    a.save();
    
    
    if a.credentials.user_callback_page:
        return HttpResponseRedirect(a.credentials.user_callback_page)
    else:
        return render(request, 'restapi/callback.html', {})        
       


def fetch_access_token(request, sessionid):
    print "Fetch access token \n"
                
    try:       
        auth = AuthSession.objects.get(session_id = sessionid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    access_token = auth.access_token
    refresh_token = auth.refresh_token
    json_response = json.dumps({"access_token": access_token, "refresh_token":refresh_token})
    
    return HttpResponse(json_response, "application/json")
        

def refresh_access_token(request, appid):
    
    credential_uid = appid
    args = dict(request.REQUEST.iteritems())
        
    try:       
        credentials = AppCredentials.objects.get(uid=credential_uid)
    except AppCredentials.DoesNotExist:
        return HttpResponse(content="Application identifier not found", status=404)
       
    try:
        refresh_token = args['refresh_token']   
    except KeyError:
        return HttpResponse(content="Refresh token not provided", status=404)
        
    #provide addtional parameters needed to refresh token
     
    params = {'grant_type': "refresh_token",
              'refresh_token': refresh_token}
    
    #initialize client with needed values 
    c = Client(   
        token_endpoint = credentials.token_endpoint,       
        client_id = credentials.app_api_key,
        client_secret = credentials.app_secret,
        )                    

    #request a new access token 
    c.request_token(token_response_parser, **params)
            
    #to check if we received a new refresh token as well
    try:
        new_refresh_token = c.refresh_token
    except AttributeError:
        new_refresh_token = ""
        
     
    json_response = json.dumps({"access_token": c.access_token,
                                "refresh_token": new_refresh_token })
     
    return HttpResponse(json_response, "application/json")
    #https://accounts.google.com/o/oauth2/revoke?token={token}
    
    
# response parser for Sanction         
def token_response_parser(s):
    
        print "Data to parse: "+s
        
        try:
            print "USing JSON parser"
            val = json.loads(s)
        except ValueError:
            print "Using URL parser"
            val = dict(parse_qsl(s))
        
        return val
                                