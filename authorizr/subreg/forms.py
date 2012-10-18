from django import forms
from subapi.models import Resource
from django.forms.widgets import TextInput

class ResourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        
        for field_name in self.fields:
            field = self.fields.get(field_name)  
            
            if field:
                if type(field.widget) is forms.TextInput:
                    field.widget = forms.TextInput(attrs={
                                                          'placeholder': field.label,                                                          
                                                          'class':'input-xxlarge'})
    
            
    class Meta:
        model = Resource
        exclude = ('uid','owner','redirect_uri')      
