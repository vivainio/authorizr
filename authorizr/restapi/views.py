
import urllib
import uuid

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render


from sanction.client import Client

from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required

from appreg.models import AppCredentials, AppOwner, AuthSession

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
    

def create_session(request):
        
    scope_req = ('user_likes',)
    #scope_req = ("https://www.googleapis.com/auth/drive",                
    #             )
    '''
    scope_req = ("https://www.googleapis.com/auth/userinfo.email",
                 "https://www.googleapis.com/auth/userinfo.profile"
                 )
    '''
    
    
    args = dict(request.REQUEST.iteritems())
        
        
    try:    
        #Get Credentials used for this session     
        cred_id = args['cred_id']        
    except KeyError:
        return HttpResponse(content="Application identifier (cred_id) parameter missing", status=400)
    
    try:       
        credentials = AppCredentials.objects.get(uid=cred_id)
    except AppCredentials.DoesNotExist:
        return HttpResponse(content="Application identifier not found", status=404)
       
    #Make unique ID for request    
    uid = uuid.uuid4().hex

    #Store it to DB TODO: foreign key link to AuthSession.. api key and secret duplicated
    authSession = AuthSession(
                    session_id = uid,
                    auth_endpoint = args['auth_endpoint'],
                    access_token = '',
                    token_endpoint = args['token_endpoint'],
                    resource_endpoint = args['resource_endpoint'],
                    client_id = credentials.app_api_key,
                    client_secret = credentials.app_secret,
                    redirect_uri = args['redirect_uri']
                    )
    
    authSession.save()
    
    #Construct authentication URI using Sanction    
    c = make_client_from_auth_session(authSession)    
    url = c.auth_uri(scope_req, state = uid)
    
    return HttpResponse("sessionid=%s\nloginurl=%s"%(uid,url), "text/plain")
        
        
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
        
    return HttpResponse("You may close the browser now and return to app", "text/plain")   


def fetch_access_token(request):
    print "Fetch access token \n"
     
    try:         
        sid = request.REQUEST['sessionid']
        print "sessionid "+ sid       
    except KeyError:
        return HttpResponse(content="Session identifier (sessionid) parameter missing", status=400)
       
    try:       
        a = AuthSession.objects.get(session_id = sid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    access_token = auths.access_token
    return HttpResponse(access_token , "text/plain")

                                