
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


def make_client_from_auth_session(auth):
    c = Client(
        auth_endpoint = auth.auth_endpoint,
        token_endpoint= auth.token_endpoint,
        resource_endpoint =auth.resource_endpoint,
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
                    client_id = cred.app_api_key,
                    client_secret = cred.app_secret,
                    redirect_uri = args.get('redirect_uri', 
                                            cred.redirect_uri),
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
    url = c.auth_uri(scope, state = uid)
    
    json_response = json.dumps({"session_id": uid, "url": url})
    
    return HttpResponse(json_response, "application/json")
        
        
def login_callback(request):
    
        
    sid = request.REQUEST['state']
    
    print "sid "+ sid
    
    try:       
        a = AuthSession.objects.get(session_id = sid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
        
            
    c = make_client_from_auth_session(a)    
        
    rdict = request.REQUEST
    print "requesting token"
    print "State",rdict['state']
    d = {'code' : rdict["code"]}
    
    def tries_parser(s):
        try:
            val = json.loads(s)
        except ValueError:
            val = dict(parse_qsl(s))
        print "Parsed",val
        return val
    
    c.request_token(tries_parser, **d)
    print "token received!"
    print c
    print "google login",rdict
    
    a.access_token = c.access_token;    
    a.save();
    
    return render(request, 'restapi/callback.html', {})        
       


def fetch_access_token(request, sessionid):
    print "Fetch access token \n"
                
    try:       
        auth = AuthSession.objects.get(session_id = sessionid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    access_token = auth.access_token
    json_response = json.dumps({"access_token": access_token})
    
    return HttpResponse(json_response, "application/json")
        
    

                                