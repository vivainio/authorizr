# Create your views here.
import pickle

def dump_request(request):
	args = dict(request.REQUEST.iteritems())
	saved_verifier = args['oauth_verifier']  
	saved_token = args['oauth_token'] 
	pickle.dump( saved_verifier, open( "/tmp/save.p", "w" ) )
	pickle.dump( saved_token, open( "/tmp/save2.p", "w" ) )
	raise Exception("Please analyze request in debugger")

