import urllib
import os
import json

_HEROKU = False

_URL_PARAMS = True


_APP_ID = 'bb7af0ad9cf1440583ad7da8a44718c2'

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
    
    at = json.loads(resp)
    
    access_token = at["access_token"]
    
    print "Received data: "+access_token +"\n"
    
    if _URL_PARAMS: 
        test_url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+access_token
    else:
        test_url = " https://www.googleapis.com/drive/v2/files?access_token="+access_token 
    
    test_resp = urllib.urlopen(test_url).read()
    
    print test_resp
    
    
main()    
