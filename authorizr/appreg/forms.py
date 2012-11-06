from django import forms

from appreg.models import AppCredentials

from django.forms.widgets import TextInput






class AppCredentialForm(forms.ModelForm):

    oauth1_field_names = ["app_desc", "app_api_key", "app_secret", "auth_endpoint", "token_endpoint"]
    oauth2_field_names = ["app_desc", "app_api_key", "app_secret", "scope","auth_endpoint", "token_endpoint", "resource_endpoint", "user_callback_page"]


    def __init__(self, *args, **kwargs):
        super(AppCredentialForm, self).__init__(*args, **kwargs)
        
        def filterbyvalue(seq, value):
            for el in seq:
                if el.attribute==value: yield el
                
        
        for field_name in self.fields:
            field = self.fields.get(field_name)  
                        
            if field:
                if type(field.widget) is forms.TextInput:
                    
                    classes  = "input-xxlarge "
                                        
                    if field_name in self.oauth1_field_names:
                        classes += "oauth1 "
                        
                    if field_name in self.oauth2_field_names:
                        classes += "oauth2 "
                    
                    field.widget = forms.TextInput(attrs={
                                                          'placeholder': field.label,                                                          
                                                          'class': classes})  
                  
            
    
    class Meta:
        model = AppCredentials
        exclude = ('uid','owner','redirect_uri')
        
    
