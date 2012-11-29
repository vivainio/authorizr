import urllib
import os
import json

_HEROKU = True

_URL_PARAMS = True


#_APP_ID = '281ad6fa1f51430ea5e6d094a23c401f'

# below works on heroku atm

#_APP_ID = '486f832ea89e487cb9e3405b60632c31'
def main():
    
    if _HEROKU:    
        server_url = "http://authorizr.herokuapp.com"
        _APP_ID = "fdfe9bee210d49cea0a9044ff16d4c8f"
    else:       
        server_url = "http://127.0.0.1:8000"
        _APP_ID = "3ec5a98706854d809fa650b71743fb88"
    
    url= ''
    
    if _URL_PARAMS:
        tg = urllib.urlencode( {
            'access_type': 'offline',
            'approval_prompt':'force',           
         })
        url = server_url+"/api/v1/create_session/"+_APP_ID+"/?"+tg     
         
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
            


    raw_input("Press enter to open URL")
    os.system('xdg-open "%s"'%url)
    
    
    access_token_url = server_url+"/api/v1/fetch_access_token/"+sid+"/"    
    
    print "access token url: "+ access_token_url +"\n"
    
    raw_input("Press enter to fetch access token")
    
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
   
    raw_input("Press enter to load data from google")
   
     
    test_url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+access_token
    
    test_resp = urllib.urlopen(test_url).read()
    print test_resp
            
main()    
