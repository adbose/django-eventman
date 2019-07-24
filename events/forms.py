from django import forms
from events.models import Event, Team


class EventForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(EventForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].required = False
    #     self.fields['result'].required = False

    class Meta:
        model = Event
        fields = ['event_name']


class ParticipationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipationForm, self).__init__(*args, **kwargs)
        self.fields['event'].required = False

    class Meta:
        model = Team
        fields = ['team_name']
