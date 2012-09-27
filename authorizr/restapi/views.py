
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
        
    scope_req = ("https://www.googleapis.com/auth/drive",                
                 )
    '''
    scope_req = ("https://www.googleapis.com/auth/userinfo.email",
                 "https://www.googleapis.com/auth/userinfo.profile"
                 )
    '''
    
    args = dict(request.REQUEST.iteritems())
    
    #Get Credentials used for this session     
    cred_id = args['cred_id']    
    credentials = AppCredentials.objects.get(uid=cred_id)
        
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
    
    a = AuthSession.objects.get(session_id = sid)
            
    c = make_client_from_auth_session(a)    
        
    rdict = request.REQUEST
    print "requesting token"
    print "State",rdict['state']
    d = {'code' : rdict["code"]}
    c.request_token(None, **d)
    print "token received!"
    print c
    print "google login",rdict
    
    a.access_token = c.access_token;    
    a.save();
        
    return HttpResponse("You may close the browser now and return to app", "text/plain")   


def fetch_access_token(request):
    print "Fetch access token \n"
    
    sid = request.REQUEST['sessionid']
    print "sessionid "+ sid
    
    auths = AuthSession.objects.get(session_id = sid)
    access_token = auths.access_token
    return HttpResponse(access_token , "text/plain")

                               