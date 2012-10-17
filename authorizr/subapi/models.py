from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    
    resource_id = models.CharField(primary_key = True, max_length = 1024)
    owner = models.ForeignKey(User)
    
    description  = models.CharField(max_length = 1024)
    sub_duration = models.IntegerField()
    sub_max_use_count = models.IntegerField()

class Subscription(models.Model):
    
    resource = models.ForeignKey(Resource)
    
    client_id = models.CharField(primary_key = True, max_length = 1024)
    description  = models.CharField(max_length = 1024)
    use_counter = models.IntegerField()
    sub_max_use_count = models.IntegerField()
    expires = models.DateTimeField()    
    