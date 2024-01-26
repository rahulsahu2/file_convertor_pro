# forms.py

from django import forms
from .models import ReceiptFile

class ReceiptFileForm(forms.ModelForm):
    class Meta:
        model = ReceiptFile
        fields = ['file']
