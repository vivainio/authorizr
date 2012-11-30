from django.contrib import admin
from appreg.models import AppCredentials, AuthSession, OAuth1AppCredentials, OAuth1Session

admin.site.register(AppCredentials)
admin.site.register(AuthSession)
admin.site.register(OAuth1AppCredentials)
admin.site.register(OAuth1Session)

