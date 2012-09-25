# Create your views here.

import urllib
import uuid

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render


from sanction.client import Client

from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required


from models import AppCredentials, AppOwner, AuthSession


config = {
          'google.client_id': "1037435290190.apps.googleusercontent.com",
          'google.client_secret' : "1AG4Y2knGVYBvuPHi1sEFpJ8"
          
          }

def frontpage(request):
    tg = urllib.urlencode( {
        "auth_endpoint":"https://accounts.google.com/o/oauth2/auth",
        "token_endpoint":"https://accounts.google.com/o/oauth2/token",
        "resource_endpoint":"https://www.googleapis.com/oauth2/v1",
        "redirect_uri": "http://localhost:8000/login/google" })
    
    url = "create_session?" + tg
    print tg                          
    return render(request, 'index.html')


@login_required
def myapps(request):       
    #user=request.user
    appOwner = AppOwner.objects.filter(uid = 'app_owner_uid')    
    credentials = AppCredentials.objects.filter(owner = appOwner)
    print 'Credentials', len(credentials)
    print credentials
    
    return render(request, 'appreg/myapps.html', {'credentials': credentials})

    #return render_to_response('appreg/myapps.html', {'credentials': credentials})




def mkclient(args):
  
  
    c = Client(auth_endpoint=args['auth_endpoint'],
    token_endpoint=args['token_endpoint'],
    resource_endpoint=args['resource_endpoint'],
    client_id=config["google.client_id"],
    client_secret=config["google.client_secret"],
    redirect_uri=args['redirect_uri'])
    
    return c


def create_session(request):
    scope_req = ("https://www.googleapis.com/auth/userinfo.email",
                 "https://www.googleapis.com/auth/userinfo.profile"
                 )
    
    args = request.REQUEST
    
    #session_id = 666
    
    uid = uuid.uuid4().hex
    
    #args['session_id'] = uid
    #session_id=uid,
    
    authSession = AuthSession(
                    session_id = uid,
                    auth_endpoint=args['auth_endpoint'],
                    access_token = '',
                    token_endpoint=args['token_endpoint'],
                    resource_endpoint=args['resource_endpoint'],
                    client_id=config["google.client_id"],
                    client_secret=config["google.client_secret"],
                    redirect_uri=args['redirect_uri']
                    )
    
    authSession.save()
    
    c = mkclient(args)
    url = c.auth_uri(scope_req, state = uid)
    
    return HttpResponse("sessionid=%s\nloginurl=%s"%(uid,url), "text/plain")


def startlogin(request):
    scope_req = ("https://www.googleapis.com/auth/userinfo.email",
                 "https://www.googleapis.com/auth/userinfo.profile"
                 )
    
    c = mkclient()
    url = c.auth_uri(scope_req, state = uid)
    
    return render_to_response("appreg/startlogin.html", { "loginurl" : url})
    
    
def logout_view(request):
  auth.logout(request)
  # Redirect to a success page.
  return HttpResponseRedirect("/")
    
        
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
    
    data = c.request("/userinfo")
    print "Got data",data
    
    return HttpResponse("Works", "text/plain")   
    