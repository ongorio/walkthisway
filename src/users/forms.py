from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    v_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('Email already Registered!')

        return email
    
    def clean_v_password(self):
        password = self.cleaned_data['password']
        v_password = self.cleaned_data['v_password']

        if password != v_password:
            raise forms.ValidationError('Passwords Don\'t Match!')
        
        return v_password

