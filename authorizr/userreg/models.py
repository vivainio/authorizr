from django.db import models
from django.contrib.auth.models import User


class OIConnectUser(User):
    user_id = models.CharField(primary_key = True, max_length = 255) 
    access_token = models.CharField(max_length=100)
    expires = models.FloatField(default=-1)


'''
{u'family_name': u'Salento',
 u'name': u'Ilkka Salento',
  u'locale': u'fi',
   u'gender': u'male', 
   u'email': u'isalento@gmail.com', 
   u'link': u'https://plus.google.com/109784351796539945220', 
   u'given_name': u'Ilkka', 
   u'id': u'109784351796539945220',
    u'verified_email': True}
    
'''