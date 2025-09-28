from django import forms
from .models import MoviePetition

class MoviePetitionForm(forms.ModelForm):
    class Meta:
        model = MoviePetition
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter movie title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Why should this movie be added to our catalog?', 
                'rows': 4
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title