from django.contrib.auth.models import User

from userreg.models import OIConnectUser 

class OIConnectAuthenticationBackend(object):
    def authenticate(self, user_info):
        print "Authenticate backend"
        try:
            user_id = user_info["id"];
                        
            oi_user = OIConnectUser.objects.get(user_id=user_id)           
            return oi_user
        except OIConnectUser.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        print "get_user backend"
        print user_id
        
        try:
            #return OIConnectUser.objects.get(pk=user_id)
            return OIConnectUser.objects.get(user_ptr_id=user_id)
        except OIConnectUser.DoesNotExist:
            print "user not found"
            return None


