# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect

from django.shortcuts import render_to_response,render, get_object_or_404

from django.template import Context

from django.contrib import auth
from django.contrib.auth.models import User 

from django.contrib.auth.decorators import login_required

from models import AppCredentials, AppOwner, AuthSession


from forms import AppCredentialForm

from django.views.generic.list import ListView
import uuid

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


def edit_app_credentials(request, appuid):
    
    cred = get_object_or_404(AppCredentials, uid=appuid)
    
    if request.method == "POST":
        form = AppCredentialForm(request.POST, instance=cred)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/appreg/editapp/'+appuid)
    else:
        form = AppCredentialForm(instance=cred)
        
    context = Context({'app_desc': cred.app_desc, 'form': form})
    
    return render(request, 'appreg/credform.html', context)

def add_application(request):
    uid = uuid.uuid4().hex
    # xxx fix
    owner = AppOwner.objects.all()[0]
    cred = AppCredentials(
        uid = uid,
        app_desc = "",
        app_api_key = "",
        app_secret = "",
        owner = owner)
    cred.save()
    return HttpResponseRedirect("/appreg/editapp/" + uid)
    
    
   
    