# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import Resource, Subscription
from datetime import timedelta, datetime

import json

def consume(request, resourceid, clientid):
    print "Fetch access token \n"
                 
    try:
        subscription = Subscription.objects.get(resource=resourceid, client_id=clientid)
    except Subscription.DoesNotExist:
        newSubs(resourceid, clientid)
        subscription = Subscription.objects.get(resource=resourceid, client_id=clientid)
    
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
    
    try:
        parentRes = Resource.objects.get(resource_id=resid)
    except Resource.DoesNotExist:
        return HttpResponse(content="Resource not found", status=404)
    #TODO validate clientid
    
    expirity = datetime.today() + timedelta(seconds=parentRes.sub_duration)

    subs = Subscription(resource=parentRes, 
                        client_id = clientid, 
                        use_counter = parentRes.sub_max_use_count, 
                        expires = expirity )
    subs.save()
   