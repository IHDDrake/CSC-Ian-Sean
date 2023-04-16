from django import forms
from .models import Event, Comment, Boat, Registration


#Form for adding Comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'cols': 130}),
        }

class BoatForm(forms.ModelForm):
    class Meta:
        model = Boat
        exclude = ["owner"]

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
        