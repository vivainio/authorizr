# Create your views here.

from django.http import HttpResponse
from models import Resource, Subscription
import time
from django.shortcuts import get_object_or_404
import json
import django.http

    
def consume(request, resourceid):
    args = dict(request.REQUEST.iteritems())
    clientid = args['client']
    credits_par = 1
    
    #credits validation (value needs to be > 0)
    try:
        if args.has_key('credits'):
            credits_par = int(args['credits'])
    except ValueError:
        return django.http.HttpResponseBadRequest()
            
    if(credits_par <= 0):
        return django.http.HttpResponseBadRequest()
         
    #credits validation end
    
    res = get_object_or_404(Resource, resource_id = resourceid)             
    
    try:        
        subscription = Subscription.objects.get(resource = res, client_id=clientid)
    except Subscription.DoesNotExist:
        newSubs(resourceid, clientid)
        subscription = get_object_or_404(Subscription, resource=res, client_id=clientid)
    
    credits_count = subscription.credits_count
    if( credits_count == None):
        credits_count = -1
    
    if (credits_count>credits_par):
        credits_count -= credits_par
    else: 
        credits_count = 0
        
    subscription.credits_count = credits_count    
    
    timestamp = subscription.expires  
    if timestamp == -1:
        expires = -1
    else:          
        expires = timestamp - time.time()
        if (expires <= 0):
            expires = 0    
          
    subscription.save()
    
    json_response = json.dumps({"credits_remaining": subscription.credits_count,
                                "time_remaining": int(expires) })
    
    return HttpResponse(json_response, "application/json")

def newSubs(resid, clientid):
    
    try:
        parentRes = Resource.objects.get(resource_id=resid)
    except Resource.DoesNotExist:
        return HttpResponse(content="Resource not found", status=404)
    #TODO validate clientid
    duration = parentRes.sub_duration 
    if ( duration == None ):
        timestamp = -1
    else:      
        timestamp = time.time() + duration
    subs = Subscription(resource=parentRes, 
                        client_id = clientid, 
                        credits_count = parentRes.sub_max_credits_count, 
                        expires = timestamp )
    subs.save()
   