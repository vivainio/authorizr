from django import forms

from appreg.models import AppCredentials

from django.forms.widgets import TextInput






class AppCredentialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AppCredentialForm, self).__init__(*args, **kwargs)
        
        for field_name in self.fields:
            field = self.fields.get(field_name)  
            
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={
                                                          'placeholder': field.label,                                                          
                                                          'class':'input-xxlarge'})    
    
    class Meta:
        model = AppCredentials
        exclude = ('uid','owner',)
        
    
