from django.db import models

# Create your models here.

class AppOwner(models.Model):
    uid = models.CharField(primary_key = True, max_length = 255)    
    desc = models.CharField(max_length = 255)
    

class AppCredentials(models.Model):
    app_desc = models.CharField(max_length = 255)
    app_api_key = models.CharField(max_length = 255)
    app_secret = models.CharField(max_length = 255)
    owner = models.ForeignKey(AppOwner)
    
    
