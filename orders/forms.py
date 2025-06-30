from django import forms
from django.forms import modelform_factory
from .models import Order, OrderProduct


class OrderAdd(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['created','updated']
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control bg-body-secondary',"id":"id_first_name","placeholder":"First Name"}),
            'last_name':forms.TextInput(attrs={'class':'form-control bg-body-secondary',"id":"id_last_name","placeholder":"Last Name"}),
            'email':forms.EmailInput(attrs={'class':'form-control bg-body-secondary',"id":"id_email","placeholder":"Email"}),
            'number':forms.TextInput(attrs={'class':'form-control bg-body-secondary',"id":"id_number","placeholder":"Number"}),
            'postal_code':forms.TextInput(attrs={'class':'form-control bg-body-secondary','id':'floatingInputValue1'}),
            'city':forms.TextInput(attrs={'class':'form-control bg-body-secondary','id':'floatingInputValue2'}),
            'post':forms.RadioSelect(attrs={'class':'form-check-input','id':'gridRadios1'}),
            'paid':forms.RadioSelect(attrs={'class':'form-check-input','id':'gridRadios2'},)
        }
