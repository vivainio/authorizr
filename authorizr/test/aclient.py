import urllib
import os


_HEROKU = False

def main():
    
    if _HEROKU:    
        server_url = "http://authorizr.herokuapp.com/"
    else:
        server_url = "http://127.0.0.1:8000"
       
    tg = urllib.urlencode( {
        "auth_endpoint":"https://accounts.google.com/o/oauth2/auth",
        "token_endpoint":"https://accounts.google.com/o/oauth2/token",
        "resource_endpoint":"https://www.googleapis.com/oauth2/v1",
        "redirect_uri": server_url+"/login/google",
        "scope": "https://www.googleapis.com/auth/drive",
        "cred_id": "100" })
        
    url = server_url+"/api/v1/create_session?"+tg
    
    print "URL to open: "+url+"\n"                        
    
    d = urllib.urlopen(url)
    print d.getcode()
    
    data = d.read()

    print "Received data: "+data +"\n"
        
    
    rows = data.split("\n")
    
    dummy,sid = rows[0].split("=",1)
    dummy,url = rows[1].split("=",1)
    
    print sid, url
            


    os.system('xdg-open "%s"'%url)
    
    raw_input("Press enter")
    
    access_token_url = server_url+"/api/v1/fetch_access_token/#?sessionid="+sid    
    
    
    access_token = urllib.urlopen(access_token_url).read()
    
    
    print "Received data: "+access_token +"\n"
     
    test_url = " https://www.googleapis.com/drive/v2/files?access_token="+access_token 
    #test_url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+access_token
    
    test_resp = urllib.urlopen(test_url).read()
    
    print test_resp
    
    
main()    
