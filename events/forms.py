from django import forms
from models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'start_date', 'start_time', 'location', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span5', 'autocomplete': 'off', 'placeholder': 'Name of event?'}),
            'start_date': forms.DateInput(attrs={'autocomplete': 'off', 'id': 'dp1', }, format='%m/%d/%Y'),
            'location': forms.TextInput(attrs={'class': 'span5', 'placeholder': 'Where is the event?', 'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'class': 'span5', 'rows': '3', 'autocomplete': 'off', 'placeholder': 'What is happening?'})
        }
    time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']
    start_time = forms.TimeField(input_formats=time_formats,
                                 required=False,
                                 widget=forms.TimeInput(attrs={'id':'timeTypeahead', 'autocomplete': 'off', 'placeholder': 'Add a time?'},format='%I:%M %p'))