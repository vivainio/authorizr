from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import string
import re

def validate_res(value):
    if re.match("^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$", value) is None:
        raise ValidationError('Resource name must use following notation [ascii string].[ascii string]...')


class Resource(models.Model):
    id = models.AutoField(primary_key = True)
    resource_id = models.CharField(unique = True, max_length = 1024)
    owner = models.ForeignKey(User)
    
    description  = models.CharField(max_length = 1024)
    sub_duration = models.PositiveIntegerField(null=True, blank=True)
    sub_max_use_count = models.PositiveIntegerField(null=True, blank = True)

class Subscription(models.Model):
    
    resource = models.ForeignKey(Resource)
    
    client_id = models.CharField(primary_key = True, max_length = 1024)
    use_counter = models.PositiveIntegerField(null=True, blank = True)
    expires = models.PositiveIntegerField(null=True, blank = True)   
    