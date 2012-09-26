# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render

from django.contrib import auth
from django.contrib.auth.models import User 

from django.contrib.auth.decorators import login_required

from models import AppCredentials, AppOwner, AuthSession


def frontpage(request):   
    return render(request, 'index.html')

def startlogin(request):
    return render(request, "appreg/startlogin.html", { "loginurl" : '' })
    
def logout_view(request):
  auth.logout(request)
  # Redirect to a success page.
  return HttpResponseRedirect("/")
  
  
@login_required
def myapps(request):       
    #user=request.user
    appOwner = AppOwner.objects.filter(uid = 'myuid')    
    credentials = AppCredentials.objects.filter(owner = appOwner)
    print 'Credentials', len(credentials)
    print credentials
    
    return render(request, 'appreg/myapps.html', {'credentials': credentials})

    #return render_to_response('appreg/myapps.html', {'credentials': credentials})

        