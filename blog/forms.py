from django import forms
from .models import Event, Comment, Boat


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
        