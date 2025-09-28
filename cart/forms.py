# cart/forms.py
from django import forms
from .models import CheckoutFeedback

class CheckoutFeedbackForm(forms.ModelForm):
    anonymous = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Submit anonymously"
    )
    
    class Meta:
        model = CheckoutFeedback
        fields = ['anonymous', 'username', 'feedback']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name (optional)'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your checkout experience...'}),
        }
        labels = {
            'username': 'Display Name',
            'feedback': 'Your Feedback',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If user is authenticated, set initial username to their username
        if 'initial' in kwargs and 'user' in kwargs['initial']:
            user = kwargs['initial']['user']
            if user.is_authenticated:
                self.fields['username'].initial = user.username