from django.contrib import admin
from appreg.models import AppCredentials, AuthSession

admin.site.register(AppCredentials)
admin.site.register(AuthSession)