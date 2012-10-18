from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    
    resource_id = models.CharField(primary_key = True, max_length = 1024)
    owner = models.ForeignKey(User)
    
    description  = models.CharField(max_length = 1024)
    sub_duration = models.PositiveIntegerField(null = True, blank = True)
    sub_max_use_count = models.PositiveIntegerField(null = True, blank = True)

class Subscription(models.Model):
    
    resource = models.ForeignKey(Resource)
    
    client_id = models.CharField(primary_key = True, max_length = 1024)
    description  = models.CharField(max_length = 1024)
    use_counter = models.IntegerField()
    expires = models.DateTimeField()    
    