# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render, get_object_or_404
from models import Resource, Subscription

import json

def consume(request, resourceid):
    print "Fetch access token \n"
           
    try:
        resource = Subscription.objects.get(resource=resourceid)
    except Subscription.DoesNotExist:
        return HttpResponse(content="Resource not found", status=404)
    
    count = resource.use_counter
    if (count>0):
        count -= 1 
        resource.use_counter = count           
    expirity = resource.expires
    resource.save()
        
    json_response = json.dumps({"uses_left": resource.use_counter,
                                "expires": expirity.strftime('%Y-%m-%dT%H:%M:%S') })
    
    return HttpResponse(json_response, "application/json")
