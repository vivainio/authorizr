# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render_to_response,render

from models import AppCredentials

from sanction.client import Client

import urllib

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
    
    
                          
    return render(request, 'appreg/index.html')

def myapps(request):    
    return render_to_response('appreg/myapps.html', {'request': request})

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
    
    
    