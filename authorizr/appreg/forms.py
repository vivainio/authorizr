from django import forms
from appreg.models import AppCredentials

class AppCredentialForm(forms.ModelForm):
    class Meta:
        model = AppCredentials
        exclude = ('uid','owner',)
        

    
