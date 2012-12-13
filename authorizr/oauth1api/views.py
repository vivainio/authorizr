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
    oauth_hook = OAuthHook()
    print "consumer key ",credentials.consumer_key    
    print "consumer secret ",credentials.consumer_secret

      
    oauth_hook.header_auth = True
    print "redirect_uri",credentials.redirect_uri
    client = requests.session(hooks={'pre_request': oauth_hook})   
    response = client.post(credentials.request_token_endpoint, data={'oauth_callback': credentials.redirect_uri + "?az_session_id=" + uid})
    
    print response
    assert(response.status_code == 200)
    response = parse_qs(response.content)
    assert(response['oauth_token'])
    assert(response['oauth_token_secret'])

    oauth_token = response['oauth_token']
    oauth_secret = response['oauth_token_secret']
    
    # Step 2: Redirecting the user auth_endpoint
    url = credentials.authorize_url+"?oauth_token="+oauth_token[0]
      
    json_response = json.dumps({"session_id": uid, "url": url})
    
    return HttpResponse(json_response, "application/json")


def login_callback(request):    
    print "login_callback"

    sid = request.REQUEST["az_session_id"]
    try:
        a = OAuth1Session.objects.get(session_id = sid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)

    a.oauth_verifier= request.REQUEST["oauth_verifier"]
    a.oauth_token = request.REQUEST["oauth_token"]
    a.save()

    #return HttpResponseRedirect(content="You can close your browser window now", status=400)
    return HttpResponseRedirect(a.credentials.user_callback_page)

def fetch_request_token(request, sessionid):             
    try:       
        auth = OAuth1Session.objects.get(session_id = sessionid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)
    
    json_response = json.dumps({"oauth_token": auth.oauth_token, "oauth_verifier":auth.oauth_verifier,
                                "consumer_key":auth.credentials.consumer_key, "consumer_secret":auth.credentials.consumer_secret})
    
    return HttpResponse(json_response, "application/json")

def fetch_access_token(request, sessionid):             
    try:       
        auth = OAuth1Session.objects.get(session_id = sessionid)
    except AuthSession.DoesNotExist:
        return HttpResponse(content="Session not found", status=404)

    OAuthHook.consumer_key = auth.credentials.consumer_key
    OAuthHook.consumer_secret = auth.credentials.consumer_secret
    oauth_hook = OAuthHook()
    
    oauth_hook.header_auth = True
    client = requests.session(hooks={'pre_request': oauth_hook})   

    response = client.post(auth.credentials.access_token_endpoint, {'oauth_verifier': auth.oauth_verifier, 'oauth_token': auth.oauth_token})
    print response
    response = parse_qs(response.content)
    assert(response['oauth_token'])
    assert(response['oauth_token_secret'])
    
    gotToken = response['oauth_token'][0]
    gotSecret = response['oauth_token_secret'][0]
    print gotToken
    print gotSecret   
    
    json_response = json.dumps({"access_token": gotToken, "access_token_secret":gotSecret,
                                "consumer_key":auth.credentials.consumer_key, "consumer_secret":auth.credentials.consumer_secret})
    
    return HttpResponse(json_response, "application/json")





