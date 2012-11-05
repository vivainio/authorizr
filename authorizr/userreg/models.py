from django.db import models
from django.contrib.auth.models import User


class OIConnectUser(User):
    user_id = models.CharField(unique=True,max_length = 255) 
    access_token = models.CharField(max_length=100)



