# Create your views here.

from django.http import HttpResponse
from models import Resource, Subscription
import time
from django.shortcuts import get_object_or_404
import json
from django.http import Http404

def consume(request, resourceid):
    args = dict(request.REQUEST.iteritems())
    clientid = args['client']
    count_par = 1
    
    #count validation (value needs to be > 0)
    try:
        if args.has_key('count'):
            count_par = int(args['count'])
    except ValueError:
        raise Http404
            
    if(count_par <= 0):
        raise Http404
         
    #count validation end
    
    res = get_object_or_404(Resource, resource_id = resourceid)             
    
    try:        
        subscription = Subscription.objects.get(resource = res, client_id=clientid)
    except Subscription.DoesNotExist:
        newSubs(resourceid, clientid)
        subscription = get_object_or_404(Subscription, resource=res, client_id=clientid)
    
    count = subscription.use_counter
    if( count == None):
        count = -1
    
    if (count>count_par):
        count -= count_par
    else: 
        count = 0
        
    subscription.use_counter = count    
    
    timestamp = subscription.expires  
    if timestamp == -1:
        expires = -1
    else:          
        expires = timestamp - time.time()
        if (expires <= 0):
            expires = 0    
          
    subscription.save()
    
    json_response = json.dumps({"uses_left": subscription.use_counter,
                                "expires": int(expires) })
    
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
                        use_counter = parentRes.sub_max_use_count, 
                        expires = timestamp )
    subs.save()
   