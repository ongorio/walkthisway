from django import forms

from django.contrib.auth import authenticate

class CustomerEditForm(forms.Form):
    email = forms.EmailField(label='Email', disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=255, label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    


class PasswordUpdateForm(forms.Form):
    original_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_original_password(self):
        old_password = self.cleaned_data['original_password']

        if not self.user.check_password(old_password):
            raise forms.ValidationError('Incorrect Password')

        return old_password

    def clean(self):
        cleaned_data = self.cleaned_data

        new_password = cleaned_data['new_password']
        confirm_password = cleaned_data['confirm_password']

        if new_password != confirm_password:
            raise forms.ValidationError('Passwords Don\'t match!')