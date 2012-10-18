# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response,render
from subapi.models import Resource, Subscription
from subreg.forms import ResourceForm

from django.template import Context

from django.views.generic.list import ListView


class ResourcesListView(ListView):
    model = Subscription
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
            return HttpResponseRedirect('/subreg/myresources/')
    else:
        form = ResourceForm()
        
    context = Context({'title': 'Add Resource', 'btn_text':'Add', 'form': form})
    return render(request, 'subreg/resourceform.html', context)  
