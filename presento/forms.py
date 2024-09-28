# forms.py
from django import forms
from .models import Presento

class PresentoForm(forms.ModelForm):
    class Meta:
        model = Presento
        fields = ['title', 'pptx_file']