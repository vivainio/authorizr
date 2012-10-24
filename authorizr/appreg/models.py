from django.db import models
from django.contrib.auth.models import User
import time
# Create your models here.
'''
class AppOwner(models.Model):

    def __unicode__(self):
        return self.desc
    
    #user = models.ForeignKey(User)    
    uid = models.CharField(primary_key = True, max_length = 255)    
    desc = models.CharField(max_length = 255)
    
  '''  

# override default manager. 
class AppCredentialsManager(models.Manager):
    def for_user(self, user):
        print user 
        return self.get_query_set().filter(owner=user.pk)
    

class AppCredentials(models.Model):
    
    def __unicode__(self):
        return self.app_desc
        
    uid = models.CharField(primary_key = True, max_length = 255)
    app_desc = models.CharField(max_length = 255)
    app_api_key = models.CharField(max_length = 255)
    app_secret = models.CharField(max_length = 255)
    
    scope = models.CharField(max_length = 1024, blank=True)    
    auth_endpoint = models.CharField(max_length = 255, blank=True)
    token_endpoint = models.CharField(max_length = 255, blank=True)
    resource_endpoint = models.CharField(max_length = 255, blank=True)
        
    redirect_uri = models.CharField(max_length = 255, blank=True) #fixed to Authorizr URL    
    user_callback_page = models.CharField(max_length = 255, blank=True) #points to users page
            
    owner = models.ForeignKey(User)
            
    objects = models.Manager() # The default manager.
    users_objects = AppCredentialsManager() # The user-specific manager.
    
class AuthSession(models.Model):
    created_at = models.PositiveIntegerField(default=time.time())
    session_id = models.CharField(primary_key = True,max_length = 255)
    access_token = models.CharField(max_length = 255)
    refresh_token = models.CharField(max_length = 255)
    #auth_endpoint = models.CharField(max_length = 255)
    #client_id = models.CharField(max_length = 255)
    #client_secret = models.CharField(max_length = 255)
    #token_endpoint = models.CharField(max_length = 255)
    #resource_endpoint = models.CharField(max_length = 255)
    #redirect_uri = models.CharField(max_length = 255)   
    #user_callback_page = models.CharField(max_length = 255)
    credentials = models.ForeignKey(AppCredentials)

