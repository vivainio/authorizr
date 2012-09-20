Authorizr web service, api design

Create service:
 - on web ui, specify app id and app secret, see generated cred_id
 - cred_id is opaque handle to app id and app secret stored on server
 - cred_id also stores protocol used (only oauth2 so far) and redirect_uri

Request start login:

```
CreateSession (
	cred_id,	 
	auth_endpoint="https://accounts.google.com/o/oauth2/auth",	
    token_endpoint="https://accounts.google.com/o/oauth2/token",
    resource_endpoint="https://www.googleapis.com/oauth2/v1",
    redirect_uri="http://authorizr.biz/oauth2callback")  <== from service
)
```

RESULT:

```
sessionid=<some opaque number that acts as handle to this session>
loginurl=<the url that you should open in browser>
```

Fetch access token for session:

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

https://www.googleapis.com/oauth2/v1/userinfo#access_token_key=7777abc

NOTE: FetchAccessToken will wait until access token is available, this 
may take a while as the user will enter their credentials in web browser.

Future investigation:

- Allow non-oauth flows through email verification? Unlock services per device








