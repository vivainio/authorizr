from django import forms
from appreg.models import AppCredentials, AppOwner

class AppCredentialForm(forms.ModelForm):
    class Meta:
        model = AppCredentials
        exclude = ('uid','owner',)
        

    
