# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import Resource, Subscription

import json

def consume(request, resourceid, clientid):
    print "Fetch access token \n"
                 
    try:
        subscription = Subscription.objects.get(resource=resourceid, client_id=clientid)
    except Subscription.DoesNotExist:
        newSubs(resourceid, clientid)
    
    count = subscription.use_counter
    if (count>0):
        count -= 1 
        subscription.use_counter = count           
    expirity = subscription.expires
    subscription.save()
        
    json_response = json.dumps({"uses_left": subscription.use_counter,
                                "expires": expirity.strftime('%Y-%m-%dT%H:%M:%S') })
    
    return HttpResponse(json_response, "application/json")

def newSubs(resid, clientid):
    subs = Subscription.objects.create()
    try:
        resource = Resource.objects.get(resource=resid)
    except Resource.DoesNotExist:
        return HttpResponse(content="Resource not found", status=404)
        
    subs.resource = resource
    
    #TODO validate clientid
    subs.client_id = clientid
    subs.use_counter = resource.sub_max_use_count
    subs.save()
   