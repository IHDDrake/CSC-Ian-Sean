from django import forms
from .models import Event,  Boat, Registration


#Form for adding Comments


class BoatForm(forms.ModelForm):
    class Meta:
        model = Boat
        exclude = ["owner"]
        widgets = {
            'classification': forms.TextInput(attrs={'placeholder': 'X'}),
            'number': forms.TextInput(attrs={'placeholder': '123'})
        }
    

class RegistrationForm(forms.ModelForm):
    boat = forms.ModelChoiceField(queryset=Boat.objects.none())
    class Meta:
        model = Registration
        fields = ['user','boat', 'event']
        exclude = ("user","event")
        

    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user.id != None:
            self.fields['boat'].queryset = Boat.objects.filter(owner=user)
        