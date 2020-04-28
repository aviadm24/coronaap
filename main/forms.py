from django import forms
from django.forms import ModelForm
from .models import user

# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)


class userForm(ModelForm):
    class Meta:
        model = user
        fields = ['first_name', 'last_name', 'number', 'address']
        labels = {
            "first_name": "שם פרטי",
            "last_name": "שם משפחה",
            "number": "מס' פלאפון",
            "address": "כתובת",
        }