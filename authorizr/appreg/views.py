# Create your views here.

import urllib
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render


from sanction.client import Client

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from models import AppCredentials, AppOwner


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
    appOwner = AppOwner.objects.filter(uid = 'app_owner_uid')    
    credentials = AppCredentials.objects.filter(owner = appOwner)
    print 'Credentials', len(credentials)
    print credentials
    return render_to_response('appreg/myapps.html', {'request': request, 'credentials': credentials})




def mkclient():
    c = Client(auth_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://accounts.google.com/o/oauth2/token",
    resource_endpoint="https://www.googleapis.com/oauth2/v1",
    client_id=config["google.client_id"],
    client_secret=config["google.client_secret"],
    redirect_uri="http://localhost:8000/login/google")
    return c


def startlogin(request):
    scope_req = ("https://www.googleapis.com/auth/userinfo.email",
                 "https://www.googleapis.com/auth/userinfo.profile"
                 )
    
    c = mkclient()
    url = c.auth_uri(scope_req, state = 666)
    return render_to_response("appreg/startlogin.html", { "loginurl" : url})
    
def logout_view(request):
  auth.logout(request)
  # Redirect to a success page.
  return HttpResponseRedirect("/")
    
        
def googlelogin(request):

    c = mkclient()
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
    
    
    