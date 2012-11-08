import urllib2
from optparse import OptionParser
import threading
import time
import ConfigParser  

threads = []

class myClient:
    moro = 1
    def __init__(self, url, appID, clientID):
        self.appID = appID
        self.clientID = clientID
        self.requestTimeTotal = 0;
        self.url = url.replace('<appid>',appID).replace('<clientid>', clientID)
        self.e500 = 0 #counter for http 500 errors
        self.eother = 0 #counter for other errors
        self.reqCount = 0 #counter for succesfull requests
        
    def makeRequest(self):
        try:
            opener = urllib2.build_opener()
            request = urllib2.Request(self.url)
            start = time.time()
            resp = opener.open(request)
            resp.read()
            ttlb = time.time() - start
            self.requestTimeTotal += ttlb
            self.reqCount +=1
            
        except urllib2.HTTPError, e:
            if(e.code == 500):
                self.e500 +=1
            else:
                self.eother +=1
        
        
class myThread (threading.Thread):
    def __init__(self, threadID, requestPerClient):
        self.threadID = threadID
        self.clients = []
        self.requestPerClient = requestPerClient
        threading.Thread.__init__(self)
        
    def addClient(self, client):
        self.clients.append(client)
        
    def run(self):
        for x in range(self.requestPerClient):
            for c in self.clients:
                c.makeRequest()

parser = OptionParser()
parser.add_option("-i", "--inifile", dest="inifile",
                  help="Ini file name", type="string")

(options, args) = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read(options.inifile)

c_url = config.get('bechmark_subapi', 'url')
c_threadcount = int(config.get('bechmark_subapi', 'threadcount'))
c_appID = config.get('bechmark_subapi', 'appID')
c_clientcount = int(config.get('bechmark_subapi', 'clientsPerThread'))
c_requestperclient = int(config.get('bechmark_subapi', 'requestperclient'))

for x in range(1, c_threadcount+1):
    thread = myThread(x,c_requestperclient)
    
    for cc in range(1, c_clientcount+1):
        c = myClient(c_url,c_appID,'client_'+str(x) + "_" +str(cc))
        thread.addClient(c);
    
    threads.append(thread);
        



#start threads
print "Starting..."
start = time.time()

for x in threads:
    x.start()

for thread in threads:
    thread.join()

ttlb = time.time() - start

print "Test Ended. "


total_time = 0
total_e500 = 0
total_requests = 0
 
for thread in threads:
    for client in thread.clients:
        total_time += client.requestTimeTotal
        total_e500 += client.e500
        total_requests += client.reqCount
        


total_req_count = c_threadcount*c_clientcount*c_requestperclient;
print "Total runtime:" + str(ttlb)
print "Requests in second:" + str(total_requests/ttlb)

print "Total request count:" + str(total_req_count)
print "Total request time:" + str(total_time)
print "Avarage request time:" + str(total_time/total_requests)
print "Total HTTP 500 errors:" + str(total_e500)
print "Total succesful requests:" + str(total_requests)
    
