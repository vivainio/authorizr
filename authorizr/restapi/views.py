
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


def make_client_from_auth_session(auth):
    c = Client(
        auth_endpoint = auth.auth_endpoint,
        token_endpoint = auth.token_endpoint,
        resource_endpoint = auth.resource_endpoint,
        client_id = auth.client_id,
        client_secret = auth.client_secret,
        redirect_uri = auth.redirect_uri)        
    return c
    

def make_auth_session(cred, args, uid):
    authSession = AuthSession(
                    session_id = uid,
                    auth_endpoint = args.get('auth_endpoint', 
                                             cred.auth_endpoint),
                    access_token = '',
                    token_endpoint = args.get('token_endpoint', 
                                              cred.token_endpoint),
                    resource_endpoint = args.get('resource_endpoint', 
                                                 cred.resource_endpoint),
                    user_callback_page = args.get('user_callback_page', 
                                            cred.user_callback_page),
                    
                    client_id = cred.app_api_key,
                    client_secret = cred.app_secret,
                    redirect_uri = cred.redirect_uri,
                    )
    
    authSession.save()
    return authSession
    


def create_session(request, appid):
     
    credential_uid = appid
    args = dict(request.REQUEST.iteritems())
        
    try:       
        credentials = AppCredentials.objects.get(uid=credential_uid)
    except AppCredentials.DoesNotExist:
        return HttpResponse(content="Application identifier not found", status=404)
       
    #Make unique ID for request    
    uid = uuid.uuid4().hex
    
    auth_session = make_auth_session(credentials, args, uid)
    
    scope = tuple(args.get('scope', credentials.scope).split(" "))    
    
    #Construct authentication URI using Sanction    
    c = make_client_from_auth_session(auth_session)    
    
    #custom parameters so that we can get refresh_token
    #google calls this offline access
    params = {'access_type': 'offline',
              'approval_prompt':'force'}
    
    
    url = c.auth_uri(scope, state = uid,**params)
      
    json_response = json.dumps({"session_id": uid, "url": url})
    
    return HttpResponse(json_response, "application/json")
        
        
def login_callback(request):
    
        
    sid = request.REQUEST['state']
    
    print "SID: "+ sid
    
    try:       
        a = AuthSession.objects.get(session_id = sid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
        
            
    c = make_client_from_auth_session(a)    
        
    rdict = request.REQUEST
    print "REQUEST:"
    print rdict
        
    d = {'code' : rdict["code"]}
       
    c.request_token(token_response_parser, **d)
    
    print "token received!"
    print c.access_token
             
    try:
        print "refresh token received!: "+ c.refresh_token
        a.refresh_token = c.refresh_token
    except AttributeError:
        print "no refresh token here"
            
    a.access_token = c.access_token;    
    
    a.save();
    
    
    if a.user_callback_page:
        return HttpResponseRedirect(a.user_callback_page)
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
                                