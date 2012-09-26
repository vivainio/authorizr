
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

'''
config = {
          'google.client_id': "1037435290190.apps.googleusercontent.com",
          'google.client_secret' : "1AG4Y2knGVYBvuPHi1sEFpJ8"          
          }
'''
def mkclient(args):
  
  
    c = Client(auth_endpoint=args['auth_endpoint'],
    token_endpoint=args['token_endpoint'],
    resource_endpoint=args['resource_endpoint'],
    client_id=args["client_id"],
    client_secret=args["client_secret"],
    redirect_uri=args['redirect_uri'])
    
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
    
    
    cred_id = args['cred_id']
    
    credentials = AppCredentials.objects.get(uid=cred_id)
        
    uid = uuid.uuid4().hex
    
    #args['session_id'] = uid
    #session_id=uid,
    
    authSession = AuthSession(
                    session_id = uid,
                    auth_endpoint=args['auth_endpoint'],
                    access_token = '',
                    token_endpoint=args['token_endpoint'],
                    resource_endpoint=args['resource_endpoint'],
                    client_id=credentials.app_api_key,
                    client_secret=credentials.app_secret,
                    redirect_uri = args['redirect_uri']
                    )
    
    authSession.save()
    
    
    args["client_id"] =credentials.app_api_key
    args["client_secret"] =credentials.app_secret
    
    
    
    c = mkclient(args)
    url = c.auth_uri(scope_req, state = uid)
    
    return HttpResponse("sessionid=%s\nloginurl=%s"%(uid,url), "text/plain")
        
def googlelogin(request):
    
    sid = request.REQUEST['state']
    print "sid "+ sid
    
    auths = AuthSession.objects.filter(session_id = sid)
    a = auths[0];
        
    c = Client(a.auth_endpoint,
    a.token_endpoint,
    a.resource_endpoint,
    a.client_id,
    a.client_secret,
    a.redirect_uri)
    
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
        
    return HttpResponse("You may close ther browser now and return to app", "text/plain")   


def fetch_access_token(request):
    print "Fetch access token \n"
    
    sid = request.REQUEST['sessionid']
    print "sessionid "+ sid
    
    auths = AuthSession.objects.filter(session_id = sid)
    a = auths[0];
    access_token = a.access_token
    return HttpResponse(access_token , "text/plain")

                               