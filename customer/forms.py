from django import forms
from accounts.models import Account


class updateuserform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name','email']