import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'phone_number', 'question']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'kiber-control',
                'placeholder': 'IDENT_NAME'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'kiber-control',
                'placeholder': '+998XXXXXXXXX',
                'minlength': '13'
            }),
            'question': forms.Textarea(attrs={
                'class': 'kiber-control',
                'rows': 5,
                'placeholder': 'ENCRYPTED_MESSAGE_PAYLOAD...'
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        clean_phone = re.sub(r'\s+', '', phone)
        pattern = r'^\+998\d{10,}$'

        if not re.match(pattern, clean_phone):
            raise ValidationError("PROTOCOL_ERROR: Invalid phone structure.")

        return clean_phone