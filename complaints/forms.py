from django import forms
from .models import Complaint
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'city', 'ward_number', 'description']
        widgets = {
            'complaint_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'ward_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)