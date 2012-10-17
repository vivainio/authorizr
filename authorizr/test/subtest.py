import urllib
import os

#HEROKU = False

def main():    
    server_url = "http://localhost:8000/"

    tg = urllib.urlencode( {
                            "resource_id" : "1",       
                            })
        
    url = server_url+"api/sub/v1/consume/res/?"+tg +"/"
    
    print "URL to open: "+url+"\n"                        
    
    d = urllib.urlopen(url)
    print d.getcode()
    
    data = d.read()

    print "Received data: "+data +"\n" 

main()  