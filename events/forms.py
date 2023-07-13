from django import forms

class EventForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    rookies_allowed = forms.BooleanField(required=False)
    free_agents_allowed = forms.BooleanField(required=False)
    active_players_allowed = forms.BooleanField(required=False)
    use_spent_limit = forms.BooleanField(required=False)
    spent_limit = forms.IntegerField(required=False)
    max_entrees = forms.IntegerField(required=False)