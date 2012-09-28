# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render

from django.contrib import auth
from django.contrib.auth.models import User 

from django.contrib.auth.decorators import login_required

from models import AppCredentials, AppOwner, AuthSession

from django.views.generic.list import ListView

def frontpage(request):   
    return render(request, 'index.html')

def startlogin(request):
    return render(request, "appreg/startlogin.html", { "loginurl" : '' })
    
def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")
  
class AppListView(ListView):
    model = AppCredentials
    template_name = "appreg/applist.html"
    def get_queryset(self):
        return self.model.objects.all()

            
  
#@login_required
def myapps(request):       
    #user=request.user
    #appOwner = AppOwner.objects.filter(uid = 'myuid')    
    #credentials = AppCredentials.objects.filter(owner = appOwner)
    
    credentials = AppCredentials.objects.all()
    
    print 'Credentials', len(credentials)
    print credentials
    
    return render(request, 'appreg/myapps.html', {'credentials': credentials})

    #return render_to_response('appreg/myapps.html', {'credentials': credentials})

#@login_required
def editapp(request, appuid):       
    #user=request.user
    #appOwner = AppOwner.objects.filter(uid = 'myuid')    
    #credentials = AppCredentials.objects.filter(owner = appOwner)
        
    print "appuid: "+ appuid
    
    credentials = AppCredentials.objects.get(uid = appuid)
    
    print 'Credentials', credentials
    
    return render(request, 'appreg/editapp.html', {'credentials': credentials})

    #return render_to_response('appreg/myapps.html', {'credentials': credentials})
    
def updateapp(request, appuid):       

    print "appuid: "+ appuid
    
    credentials = AppCredentials.objects.get(uid = appuid)
    
    credentials.app_api_key = request.POST['app_api_key']
    credentials.app_secret = request.POST['app_api_secret']
    
    credentials.save()
    print 'Credentials', credentials
        
    return HttpResponseRedirect("/appreg/editapp/"+appuid+"/")
    