# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response,render
from subapi.models import Resource, Subscription
from subreg.forms import ResourceForm

from django.template import Context

from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404


class ResourcesListView(ListView):
    model = Resource
    template_name = "subreg/reslist.html"
    
    def get_queryset(self):
        print self.request.user
        return self.model.objects.filter(owner=self.request.user)
        #return self.model.users_objects.for_user(self.request.user)
        
#def myresources(request):
    #return render(request, "subreg/myresources.html", { "loginurl" : '' })
def resource(request):
    return render(request, "subreg/resource.html", { "loginurl" : '' })
def add_resource(request):
    
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
        
            item = Resource.objects.create(

                     resource_id = form.cleaned_data['resource_id'],
                     description = form.cleaned_data['description'],
                     sub_duration = form.cleaned_data['sub_duration'],
                     sub_max_use_count = form.cleaned_data['sub_max_use_count'],
                     owner = request.user
                     )            
            return HttpResponseRedirect('/subreg/resources/')
    else:
        form = ResourceForm()
        
    context = Context({'title': 'Add Resource', 'btn_text':'Add', 'form': form})
    return render(request, 'subreg/resourceform.html', context)  


def edit_resource(request, resid):
    
    try:
        resource = Resource.objects.get(id=resid)
    except Resource.DoesNotExist:
        return HttpResponse(content="Resource not found", status=404)
    
    if request.method == "POST":
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/subreg/resources/')
    else:
        form = ResourceForm(instance=resource)
        form.fields['resource_id'].widget.attrs['readonly'] = True
        
    context = Context({'title': 'Editing Resource',
                       'btn_text':'Save',
                       'form': form})
    return render(request, 'subreg/resourceform.html', context)  

def delete_resource(request, resid):
    resource = get_object_or_404(Resource, id=resid)    
    resource.delete()

    return HttpResponseRedirect('/subreg/resources/') 
       
def subsforresource(request, resid):       
    res= get_object_or_404(Resource, id=resid)  
    subscriptions = Subscription.objects.filter(resource = res)
     
    return render(request, 'subreg/subsforresource.html', {'subscripts': subscriptions})	
