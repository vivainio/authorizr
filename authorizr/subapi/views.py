# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect

import json

def consume(request, resourceid):
    print "Fetch access token \n"
                
    if 0:
        return HttpResponse(content="Resource not found", status=404)
    
    json_response = json.dumps({"sub_time_remaining": 777 });
    
    return HttpResponse(json_response, "application/json")
