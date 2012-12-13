
import urllib
from urlparse import parse_qs
import os
import json
import random
import time
import hmac
from hashlib import md5
import urllib2
import base64

_URL_PARAMS = False

def _parse_qs(qs):
    request_params = {}
    for param in qs.split('&'):
        (request_param, request_param_value) = param.split('=')
        request_params[request_param] = request_param_value

    return request_params

class OAuthConsumerCredential:
    OAUTH_SIGNATURE_METHOD = 'HMAC-SHA1'
    OAUTH_VERSION = '1.0'
    
    # You can construct 3 kinds of OAuth credentials:
    # 1. A credential with no token (to get a request token):
    #    OAuthConsumerCredential('consumer_key', 'consumer_secret')
    #    OAuthConsumerCredential(oauth_consumer_key='consumer_key', oauth_consumer_secret='consumer_secret')
    # 2. A 3 legged OAuth credential (request or authorized token):
    #    OAuthConsumerCredential('consumer_key', 'consumer_secret', 'token', 'token_secret')
    #    OAuthConsumerCredential(oauth_consumer_key='consumer_key', oauth_consumer_secret='consumer_secret', oauth_token='token', oauth_token_secret='token_secret')
    # 3. A 2 legged OAuth credential:
    #    OAuthConsumerCredential('consumer_key', 'consumer_secret', 'requestor_id')
    #    OAuthConsumerCredential(oauth_consumer_key='consumer_key', oauth_consumer_secret='consumer_secret', oauth_requestor_id='requestor_id')
    def __init__(self, oauth_consumer_key, oauth_consumer_secret,
                 oauth_token='', oauth_token_secret='', oauth_requestor_id=''):
        self._oauth_consumer_key     = oauth_consumer_key
        self._oauth_consumer_secret  = oauth_consumer_secret
        
        self._oauth_oauth_token = self._oauth_token_secret = self._oauth_requestor_id = '' 
        if oauth_token != '' and oauth_token_secret != '':
            self._oauth_oauth_token      = oauth_token
            self._oauth_token_secret     = oauth_token_secret
        elif oauth_token != '':
            self._oauth_requestor_id = oauth_token
        elif oauth_requestor_id != '':
            self._oauth_requestor_id = oauth_requestor_id
        
    def authorize(self, request, args):
        request.add_header('Authorization',
            self._generate_authorization_header(
                request, args))
    
    def validateSignature(self, url):
        base_url, query = url.split("?", 1)
        params = {}
        def parse_param(param_string):
            name, value = param_string.split("=", 1)
            params[urllib.unquote(name)] = urllib.unquote(value)
        map(parse_param, query.split("&"))
        
        signature = params.get('oauth_signature')
        
        return signature == self._generate_signature('GET', base_url, params)

    def getOAuthConsumerKey(self):
        return self._oauth_consumer_key
    
    def getOAuthConsumerSecret(self):
        return self._oauth_consumer_secret

    def getOAuthToken(self):
        return self._oauth_oauth_token

    def getOAuthTokenSecret(self):
        return self._oauth_token_secret
    
    def getOAuthRequestorId(self):
        return self._oauth_requestor_id
    
    def getSessionParameters(self, redirect_url, action):
        params = self._generate_oauth_parameters('GET', action, {'redirect_url':redirect_url})
        params['redirect_url'] = redirect_url
        params['action'] = action
        return json.dumps(params)
    
    def _generate_authorization_header(self, request, args):
        realm = request.get_type() + '://' + request.get_host()
        http_method = request.get_method().upper()
        http_url = request.get_type() + '://' + request.get_host() + request.get_selector().split('?', 1)[0]
        return ('OAuth realm="%s",' % (realm)) + \
            ','.join(
                ['%s="%s"' % (_escape(k), _escape(v))
                 for k, v in self._generate_oauth_parameters(
                     http_method, http_url, args).items()])

    def _generate_oauth_parameters(self, http_method, http_url, args):
        oauth_parameters = {
            'oauth_consumer_key'     :
                self._oauth_consumer_key,
            'oauth_nonce'            : _generate_nonce(),
            'oauth_timestamp'        : str(int(time.time())),
            'oauth_signature_method' :
                OAuthConsumerCredential.OAUTH_SIGNATURE_METHOD,
            'oauth_version'          : OAuthConsumerCredential.OAUTH_VERSION
            }
        if self._oauth_oauth_token != '':
            oauth_parameters['oauth_token'] = \
                self._oauth_oauth_token
        
        if self._oauth_requestor_id != '':
            oauth_parameters['xoauth_requestor_id'] = \
                self._oauth_requestor_id

        oauth_parameters_for_base_string = oauth_parameters.copy()
        if args is not None:
            oauth_parameters_for_base_string.update(args)

        oauth_parameters['oauth_signature'] = self._generate_signature(http_method, http_url, oauth_parameters_for_base_string)
        
        return oauth_parameters
    
    def _generate_signature(self, method, base_url, params):
        base_url = _escape(base_url)
        
        params.pop('oauth_signature', None)
        
        parameters = _escape(
            '&'.join(
                ['%s=%s' % \
                 (_escape(str(k)), _escape(str(params[k]))) \
                 for k in sorted(params)]))

        signature_base_string = '&'.join([method, base_url, parameters])
        
        key = self._oauth_consumer_secret + '&' + self._oauth_token_secret
        
        try:
            import hashlib
            hashed = hmac.new(key, signature_base_string, hashlib.sha1)
        except ImportError:
            import sha
            hashed = hmac.new(key, signature_base_string, sha)
    
        return base64.b64encode(hashed.digest())

# } class:OAuthConsumerCredential

def _escape(s):
    return urllib.quote(str(s), safe='~')

def _generate_nonce():
    random_number = ''.join(str(random.randint(0, 9)) for _ in range(40))
    m = md5(str(time.time()) + str(random_number))
    return m.hexdigest()

class TwAuth(object):   
    def __init__(self, credential = None, api_url='https://api.twitter.com',
                 webauth_credentials = None, oauth_credentials = None):
        self._api_url     = api_url
        self._api_version = 'v1'
        self._credential  = credential or oauth_credentials or webauth_credentials

        self.resource  = None
        self.response  = None
        self.http_code = None

    def _do_request(self, verb, entity=None, url_args=None, post_args=None):
        """
        Makes a request POST/GET to the API and returns the response
          from the server.
        """
        #if verb in ['/oauth/request_token', '/oauth/access_token', '/1/statuses/update.json' ]:
        base_url = self._api_url + verb
      
        args = None
        if url_args is not None:
            args = url_args
            url = base_url + '?' + urllib.urlencode(url_args)
            print "url ", url
        else:
            url = base_url

        self.resource = url

        if post_args is not None:
            args = post_args
            request = urllib2.Request(url, urllib.urlencode(post_args))
        else:
            request = urllib2.Request(url)
            
        self._credential.authorize(request, args)
        stream = None
        try:
            stream = urllib2.urlopen(request)
            self.http_code = 200
        except urllib2.HTTPError, http_error:
            self.http_code = http_error.code
            stream = http_error

        data = stream.read()
        stream.close()
        self.response = data
        return data

   
    def get_request_token(self):
        response = self._do_request('/oauth/request_token')

        if self.http_code == 200:
            return _parse_qs(response)
        else:
            return response

    def get_access_token(self):
        response = self._do_request('/oauth/access_token')

        if self.http_code == 200:
            return _parse_qs(response)
        else:
            return response
    def do_post_request(self, p_args):
        response = self._do_request('/1/statuses/update.json', '','', p_args)

        if self.http_code == 200:
            return response
        else:
            return self.http_code

def main():
    # Step 1: Creating a request token for a new session
    server_url = "http://127.0.0.1:8000"
    _APP_ID = "4aaba2155b1a4a4d876178383b458c71"
    
    url= ''
    
    if _URL_PARAMS:
        tg = urllib.urlencode( {
            'access_type': 'offline',
            'approval_prompt':'force',           
         })
        url = server_url+"/api/oauth1/v1/create_session/"+_APP_ID+"/?"+tg     
         
    else:
        url = server_url+"/api/oauth1/v1/create_session/"+_APP_ID+"/"
    
    print "URL to open: "+url+"\n"                        
    
    d = urllib.urlopen(url)
    print d.getcode()
    
    data = d.read()   
    data = json.loads(data)
    
    sid =  data["session_id"]
    url =  data["url"]
    print "sid:",sid, " url:",url

    # Step 2: Redirecting the user
    raw_input("Press enter to open URL")
    os.system('xdg-open "%s"'%url)

    raw_input("Enter credentials in browser, and then press enter to Authenticate")

    # Step 3: Authenticate
    #get request token from Authorizr
    #fetch_tokens_url = server_url+"/api/oauth1/v1/fetch_request_token/"+sid +"/"    
    fetch_tokens_url = server_url+"/api/oauth1/v1/fetch_access_token/"+sid +"/"  
    print "fetch_tokens_url:", fetch_tokens_url
    data = urllib.urlopen(fetch_tokens_url).read()   
    data = json.loads(data)
    print data
    access_token = data["access_token"]
    access_token_secret = data["access_token_secret"]
    consumer_key = data["consumer_key"]
    consumer_secret = data["consumer_secret"]
    print "access_token from authorizr ", access_token
    print "access_token_secret from authorizr ", access_token_secret
    print "consumer_key from authorizr ", consumer_key
    print "consumer_secret from authorizr ", consumer_key
    api_url = 'https://api.twitter.com'
    
    #Converting the request token to an access token
    # api_url = 'https://api.twitter.com'   
    # authorized_token = token
    # authorized_token_secret = verifier

    # oauth_credential = OAuthConsumerCredential(consumer_key, consumer_secret, authorized_token, authorized_token_secret)
    # t = TwAuth(oauth_credential, api_url = api_url)
    # response = t.get_access_token()
    # print response
   
    # assert(response['oauth_token'])
    # assert(response['oauth_token_secret'])
    # access_token = response['oauth_token']
    # access_token_secret = response['oauth_token_secret']
    # print "access_token ", access_token
    # print "access_token_secret ", access_token_secret


    #Making authorized request
    oauth_credential = OAuthConsumerCredential(consumer_key, consumer_secret, access_token, access_token_secret)
    t = TwAuth(oauth_credential, api_url= api_url)
    message = "Random from authorizr2 %s" % random.random()
    args = {'status': message}
    response = t.do_post_request(args)
    print response

main()   

