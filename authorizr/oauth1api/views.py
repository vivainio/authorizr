# Create your views here.
import pickle
from django.http import HttpResponse,HttpResponseRedirect
from restapi import views
from appreg.models import OAuth1AppCredentials, OAuth1Session
import requests
from urlparse import parse_qs
import uuid
from oauth_hook.hook import OAuthHook
import oauth_hook
import json

def dump_request(request):
	args = dict(request.REQUEST.iteritems())
	saved_verifier = args['oauth_verifier']  
	saved_token = args['oauth_token'] 
	pickle.dump( saved_verifier, open( "/tmp/save.p", "w" ) )
	pickle.dump( saved_token, open( "/tmp/save2.p", "w" ) )
	raise Exception("Please analyze request in debugger")

def make_auth_session(cred, uid):
    authSession = OAuth1Session(
                    session_id = uid,
                    oauth_verifier = '',
                    oauth_token = '',
                    credentials = cred,
                    )
    
    authSession.save()
    return authSession

def create_session(request, appid):   
    credential_uid = appid
    
    print "creating session for: "+credential_uid
    
    args = dict(request.REQUEST.iteritems())
        
    try:       
        credentials = OAuth1AppCredentials.objects.get(uid=credential_uid)
    except OAuth1AppCredentials.DoesNotExist:
        return HttpResponse(content="Application for specified handle not found", status=404)
       
    #Make unique ID for request    
    uid = uuid.uuid4().hex
    
    #initiate db entry for this session
    auth_session = make_auth_session(credentials, uid)
    
    OAuthHook.consumer_key = credentials.consumer_key
    OAuthHook.consumer_secret = credentials.consumer_secret
    twitter_oauth_hook = OAuthHook()
        
    #for header_auth in (True, False):
    # See https://dev.twitter.com/docs/auth/implementing-sign-twitter
    # Step 1: Obtaining a request token
    #twitter_oauth_hook.header_auth = True
    oauth_hook.header_auth = True
    print credentials.redirect_uri
    client = requests.session(hooks={'pre_request': twitter_oauth_hook})   
    response = client.post(credentials.token_endpoint, data={'oauth_callback': credentials.redirect_uri + "?az_session_id=" + uid})
    
    print response
    assert(response.status_code == 200)
    response = parse_qs(response.content)
    assert(response['oauth_token'])
    assert(response['oauth_token_secret'])

    oauth_token = response['oauth_token']
    oauth_secret = response['oauth_token_secret']
    
    # Step 2: Redirecting the user auth_endpoint
    url = credentials.auth_endpoint+"?oauth_token="+oauth_token[0]
      
    json_response = json.dumps({"session_id": uid, "url": url})
    
    return HttpResponse(json_response, "application/json")


def login_callback(request):    
    print "login_callback"

    sid = request.REQUEST["az_session_id"]

    a = OAuth1Session.objects.get(session_id = sid)
    a.oauth_verifier = request.REQUEST["oauth_verifier"]
    a.oauth_token = request.REQUEST["oauth_token"]
    a.save()

    return HttpResponse(content="You can close your browser window now", status=400)

def fetch_access_token(request, sessionid):             
    try:       
        auth = OAuth1Session.objects.get(session_id = sessionid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    json_response = json.dumps({"oauth_token": auth.oauth_verifier, "oauth_token_secret":auth.oauth_token})
    
    return HttpResponse(json_response, "application/json")




