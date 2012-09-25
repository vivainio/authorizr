from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AppOwner(models.Model):

    def __unicode__(self):
        return self.desc
    
    #user = models.ForeignKey(User)    
    uid = models.CharField(primary_key = True, max_length = 255)    
    desc = models.CharField(max_length = 255)
    

class AuthSession(models.Model):
    session_id = models.CharField(primary_key = True,max_length = 255)
    access_token = models.CharField(max_length = 255)
    auth_endpoint = models.CharField(max_length = 255)
    client_id = models.CharField(max_length = 255)
    client_secret = models.CharField(max_length = 255)
    token_endpoint = models.CharField(max_length = 255)
    resource_endpoint = models.CharField(max_length = 255)
    redirect_uri = models.CharField(max_length = 255)

class AppCredentials(models.Model):
    
    def __unicode__(self):
        return self.app_desc
    
    app_desc = models.CharField(max_length = 255)
    app_api_key = models.CharField(max_length = 255)
    app_secret = models.CharField(max_length = 255)
    owner = models.ForeignKey(AppOwner)
    
    
