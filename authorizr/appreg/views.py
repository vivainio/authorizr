# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render, get_object_or_404

from django.template import Context

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import AppCredentials, AuthSession, OAuth1AppCredentials
from forms import AppCredentialFormOauth1, AppCredentialFormOauth2

from django.views.generic.list import ListView
#from myproject.apps.users.models import LoggedInMixin

import uuid
from django.core.cache import cache

#Callback URL
from django.conf import settings
import django.core.exceptions


def frontpage(request):   
    return render(request, 'index.html')
 
def login(request):
    return render(request, "appreg/login.html", { })
    
def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")
  
#ListView
class AppListView(ListView):
    model = AppCredentials
    template_name = "appreg/applist.html"
    
    def get_queryset(self):
        print self.request.user
        return self.model.objects.filter(owner=self.request.user)
        #return self.model.users_objects.for_user(self.request.user)

            
  
#@login_required
def myapps(request):       
    #user=request.user
    #appOwner = AppOwner.objects.filter(uid = 'myuid')    
    #credentials = AppCredentials.objects.filter(owner = appOwner)
    
    oa2credentials = AppCredentials.users_objects.for_user(request.user)
    oa1credentials = OAuth1AppCredentials.users_objects.for_user(request.user)
    #credentials = AppCredentials.objects.all()
    #print request.user,
    #print 'Credentials', len(credentials)
    #print credentials
    print oa1credentials
    return render(request, 'appreg/applist.html', {'oa2credentials': oa2credentials, 'oa1credentials' : oa1credentials})


def edit_app_credentials(request, appuid):
    
    editing = True
    oa1 = False
    form = None
    try :
        cred = AppCredentials.objects.get(uid=appuid)
    except django.core.exceptions.ObjectDoesNotExist:
        cred = get_object_or_404(OAuth1AppCredentials, uid=appuid)
        oa1 = True
                      
    if request.method == "POST":        
        cache.delete("cr_" + appuid)
        if (oa1):          
            form = AppCredentialFormOauth1(request.POST, instance=cred)            
        else:
            form = AppCredentialFormOauth2(request.POST, instance=cred)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/appreg/myapps/')
    
    if( form is None):
        formOauth2 = AppCredentialFormOauth2(instance=cred) 
        formOauth1 = AppCredentialFormOauth1(instance=cred)
        
        context = Context({'title': 'Editing Application:'+cred.app_desc ,
                           'btn_text':'Save',
                           'appuid': cred.uid, 
                           'formOauth1': formOauth1,
                           'formOauth2': formOauth2,
                           'editing': editing,
                           'oa1default' : oa1})
    else:
        context = Context({'title': 'Editing Application:'+cred.app_desc ,
                           'btn_text':'Save',
                           'appuid': cred.uid, 
                           'formOauth1': form,
                           'formOauth2': form,
                           'editing': editing,
                           'oa1default' : oa1})
    
    return render(request, 'appreg/credform.html', context)

def add_application(request):
    
    form = None
    if request.method == "POST":
        if 'oa1' in request.POST:

            form = AppCredentialFormOauth1(request.POST)
            oa1default = True
            if form.is_valid():                
                 # create a new item
                uid = uuid.uuid4().hex
            
                item = OAuth1AppCredentials.objects.create(
                         uid = uid,
                         app_desc = form.cleaned_data['app_desc'],
                         consumer_key = form.cleaned_data['consumer_key'],
                         consumer_secret = form.cleaned_data['consumer_secret'],
                         auth_endpoint = form.cleaned_data['auth_endpoint'],
                         token_endpoint = form.cleaned_data['token_endpoint'],                         
                         user_callback_page = form.cleaned_data['user_callback_page'],
                         redirect_uri = settings._OAUTH1_CALLBACK_URL,
                         owner = request.user
                         )               
                return HttpResponseRedirect('/appreg/myapps/')             


        elif 'oa2' in request.POST:
            form = AppCredentialFormOauth2(request.POST)
            oa1default = False
            if form.is_valid():
                 # create a new item
                uid = uuid.uuid4().hex
                
                item = AppCredentials.objects.create(
                         uid = uid,
                         app_desc = form.cleaned_data['app_desc'],
                         app_api_key = form.cleaned_data['app_api_key'],
                         app_secret = form.cleaned_data['app_secret'],
                         
                         scope = form.cleaned_data['scope'],
                         auth_endpoint = form.cleaned_data['auth_endpoint'],
                         token_endpoint = form.cleaned_data['token_endpoint'],
                         resource_endpoint = form.cleaned_data['resource_endpoint'],
                         user_callback_page = form.cleaned_data['user_callback_page'],
                         redirect_uri = settings._OAUTH2_CALLBACK_URL,
                         owner = request.user
                         )            
                return HttpResponseRedirect('/appreg/myapps/')
    
    if( form is None):
        formOauth2 = AppCredentialFormOauth2()
        formOauth1 = AppCredentialFormOauth1()        
        context = Context({'title': 'New Application', 'btn_text':'Add Application', 'formOauth2':formOauth2, 'formOauth1': formOauth1})
    else:
        context = Context({'title': 'New Application', 'btn_text':'Add Application', 'formOauth2':form, 'formOauth1': form, 'editing':True, 'oa1default':oa1default})
    return render(request, 'appreg/credform.html', context)   
  
def delete_application(request, appuid):
    
    try :
        cred = AppCredentials.objects.get(uid=appuid)
    except django.core.exceptions.ObjectDoesNotExist:
        cred = get_object_or_404(OAuth1AppCredentials, uid=appuid)
    cred.delete()
    
    return HttpResponseRedirect('/appreg/myapps/')

    