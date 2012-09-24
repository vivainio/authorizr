from django.db import models

# Create your models here.

class AppOwner(models.Model):    
    uid = models.CharField(primary_key = True, max_length = 255)    
    desc = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.desc

class AuthSession(models.Model):
    access_token = models.CharField(max_length = 255)

class AppCredentials(models.Model):
    
    def __unicode__(self):
        return self.app_desc
    
    app_desc = models.CharField(max_length = 255)
    app_api_key = models.CharField(max_length = 255)
    app_secret = models.CharField(max_length = 255)
    owner = models.ForeignKey(AppOwner)
    
    
