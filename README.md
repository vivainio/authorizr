# Authorizr web service

Problem: OAuth flows can't be comfortably executed on all 
mobile platforms (e.g. S40 web apps) because they require
an embedded web browser control (where you can intercept redirects) 
or a way to listen to a port on localhost, and have the native
browser use that port on localhost as callback.

Services like twitter can make this easier by providing a "shortcut" 
protocol like xAuth, but you have to apply for permission to use such a 
hack separately, and most services (oauth2 services, specifically) 
don't have such workarounds available.

Authorizr is a web service that cirmumvents this problem by 
executing the oauth2 handshake at an external web server. Moreover, 
Application ID and API Secret are hosted at Authorizr server,
so you don't have to ship the secret with your source code; this
makes using the service more secure, assuming that you trust the admins 
authorizr to not abuse the api secret. 


# Authorizr web service, api design

## Create service:
 - on web ui, specify app id and app secret, see generated cred_id
 - cred_id is opaque handle to app id and app secret stored on server
 - cred_id also stores protocol used (only oauth2 so far) and redirect_uri

## Request start login:

```
CreateSession (
	cred_id,	 
	auth_endpoint="https://accounts.google.com/o/oauth2/auth",	
    token_endpoint="https://accounts.google.com/o/oauth2/token",
    resource_endpoint="https://www.googleapis.com/oauth2/v1",
    
)
```

RESULT:

```
sessionid=<some opaque number that acts as handle to this session>
loginurl=<the url that you should open in browser>
```

Note how we didn't specify redirect_uri in arguments, it's configured on 
the web interface (for oauth2, 
redirect_uri="http://authorizr.biz/oauth2callback") 

## Fetch access token for session:

```
FetchAccessToken (
	session_id
)
```

RESULT:

```
access_token=<the token you can start using in your requests>
```

E.g. if access_token you got is 7777abc, you can invoke request 
for google user info:

https://www.googleapis.com/oauth2/v1/userinfo?access_token_key=7777abc

NOTE: FetchAccessToken will wait until access token is available, this 
may take a while as the user will enter their credentials in web browser.

## Future investigation:

- Allow non-oauth flows through email verification? Unlock services per device








