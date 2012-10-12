
import urllib
import uuid

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render

from django.template import Context
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
                    
    #Construct authentication URI using Sanction
    url = c.auth_uri(scope, state = uid,**args)
      
    json_response = json.dumps({"session_id": uid, "url": url})
    
    return HttpResponse(json_response, "application/json")
        
        
def login_callback(request):
    
    print "login_callback"

    args = dict(request.REQUEST.iteritems())

    #in create_session uid was sent to server as state parameter         
    try:
        sid = args['state']   
        a = AuthSession.objects.get(session_id = sid)
    except KeyError:
        return HttpResponse(content="Authorization server did not return state parameter", status=400)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    
    def respond(response):                    
        if a.credentials.user_callback_page:
           return HttpResponseRedirect(a.credentials.user_callback_page+response['user_cb_query'])
        else:           
           return render(request, 'restapi/callback.html', Context(response['msg']))
    
    success_response = { 'msg' : {'message': 'Access Granted'},
                         'user_cb_query' : "?success=true"}
    
    fail_response = { 'msg' : {'message': 'Access Denied'},    
                      'user_cb_query' : "?success=false"}
    
    
    #code is included if user granted access
    #?error=access_denied&state=43d397028ad446cab5ff77fd662eea3
    try:
        code = args['code']
    except KeyError:
        return respond(fail_response)
        
    params = {'code' : code}
           
    c = make_client(a.credentials)    
    c.request_token(token_response_parser, **params)
       
    a.access_token = c.access_token;
    
    if hasattr(c, 'refresh_token'):
        a.refresh_token = c.refresh_token        
    
    a.save();

    return respond(success_response)
        

def fetch_access_token(request, sessionid):
    print "Fetch access token \n"
                
    try:       
        auth = AuthSession.objects.get(session_id = sessionid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    json_response = json.dumps({"access_token": auth.access_token, "refresh_token":auth.refresh_token})
    
    return HttpResponse(json_response, "application/json")
        

def refresh_access_token(request, credential_uid):
     
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
        client_secret = credentials.app_secret,)                    

    #request a new access token 
    c.request_token(token_response_parser, **params)
            
    #to check if we received a new refresh token as well
    if hasattr(c, 'refresh_token'):
        new_refresh_token = c.refresh_token        
    else:
        new_refresh_token = ""
     
    json_response = json.dumps({"access_token": c.access_token,
                                "refresh_token": new_refresh_token })
     
    return HttpResponse(json_response, "application/json")
  
    
    
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
                                