from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'number', 'feedback_type', 'message']

        widgets = {
            'feedback_type': forms.Select(choices=Feedback.FEEDBACK_TYPE_CHOICES),
            'message': forms.Textarea(attrs={'rows': 5}),
        }