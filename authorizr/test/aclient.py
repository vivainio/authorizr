import urllib
import os
import json

_HEROKU = False

_URL_PARAMS = True


_APP_ID = '12968c7f11844baabe9ae48f500472f3'

def main():
    
    if _HEROKU:    
        server_url = "http://authorizr.herokuapp.com"
    else:       
        server_url = "http://127.0.0.1:8000"
    
    url= ''
    
    if _URL_PARAMS:
        tg = urllib.urlencode( {
            #"auth_endpoint":"https://accounts.google.com/o/oauth2/auth",
            #"token_endpoint":"https://accounts.google.com/o/oauth2/token",
            #"resource_endpoint":"https://www.googleapis.com/oauth2/v1",
            #"redirect_uri": server_url+"/login/oauth2callback",
            #"scope": "https://www.googleapis.com/auth/drive",
            #"scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
         })
        url = server_url+"/api/v1/create_session/"+_APP_ID+"/" 
         
         #?"+tg
         
    else:
        url = server_url+"/api/v1/create_session/"+_APP_ID+"/"
    
    print "URL to open: "+url+"\n"                        
    
    d = urllib.urlopen(url)
    print d.getcode()
    
    data = d.read()

    print "Received data: "+data +"\n"
   
    data = json.loads(data)
    
    sid =  data["session_id"]
    url =  data["url"]
    print sid, url
            


    os.system('xdg-open "%s"'%url)
    
    raw_input("Press enter")
    
    access_token_url = server_url+"/api/v1/fetch_access_token/"+sid+"/"    
    
    print "access token url: "+ access_token_url +"\n"
    
    resp = urllib.urlopen(access_token_url).read()
    
    print "Received data:" +resp

    at = json.loads(resp)
    
    access_token = at["access_token"]
    refresh_token = at["refresh_token"]
    
    refresh_token_url = server_url+"/api/v1/refresh_access_token/"+_APP_ID+"/?refresh_token="+refresh_token
    print "Refresh token URL:"    
    print refresh_token_url
    
    print "Revoke Link:"
    print "https://accounts.google.com/o/oauth2/revoke?token="+access_token
   
    if _URL_PARAMS: 
        test_url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+access_token
    else:
        test_url = " https://www.googleapis.com/drive/v2/files?access_token="+access_token 
    
    test_resp = urllib.urlopen(test_url).read()
            
main()    
