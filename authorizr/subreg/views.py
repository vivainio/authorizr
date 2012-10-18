# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response,render
from subapi.models import Resource, Subscription
from subreg.forms import ResourceForm

from django.template import Context

def myresources(request):
    return render(request, "subreg/myresources.html", { "loginurl" : '' })
def resource(request):
    return render(request, "subreg/resource.html", { "loginurl" : '' })
def add_resource(request):
    
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
            # create a new item
            #uid = uuid.uuid4().hex
        
            item = ResourceForm.objects.create(
                     #uid = uid,
                     resource_id = form.cleaned_data['resource_id'],
                     description = form.cleaned_data['description'],
                     sub_duration = form.cleaned_data['sub_duration'],
                     
                     sub_max_use_count = form.cleaned_data['sub_max_use_count'],

                     #redirect_uri = settings._CALLBACK_URL,
                     #owner = request.user
                     )            
            return HttpResponseRedirect('/subreg/myresources/')
    else:
        form = ResourceForm()
        
    context = Context({'title': 'Add Application', 'btn_text':'Add Application', 'form': form})
    return render(request, 'subreg/resourceform.html', context)  
