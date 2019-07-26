from django import forms
from events.models import Team


class ParticipationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipationForm, self).__init__(*args, **kwargs)
        self.fields['event'].required = False

    class Meta:
        model = Team
        fields = "__all__"
