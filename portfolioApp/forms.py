from django import forms
from .models import Person, Owner, Property, Flight

class PersonForm(forms.ModelForm):
    owners = forms.ModelMultipleChoiceField(
        queryset=Owner.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    properties = forms.ModelMultipleChoiceField(
        queryset=Property.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    flights = forms.ModelMultipleChoiceField(
        queryset=Flight.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Person
        fields = ['name', 'email', 'phone_number', 'owners', 'properties', 'flights']
