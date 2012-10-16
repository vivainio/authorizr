# Create your views here.

from django.http import HttpResponse

from django.http import HttpResponseRedirect


from django.shortcuts import render_to_response,render



def myresources(request):
	return render(request, "subreg/myresources.html", { "loginurl" : '' })
