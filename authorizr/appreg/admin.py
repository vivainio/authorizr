from django.contrib import admin
from appreg.models import AppOwner, AppCredentials, AuthSession

admin.site.register(AppOwner)
admin.site.register(AppCredentials)
admin.site.register(AuthSession)