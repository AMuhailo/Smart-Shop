from django import forms

class CartField(forms.Form):
    quantity = forms.CharField(initial=1,required=False, widget = forms.TextInput(attrs={'class':'form-control form-number',
                                                                               "value":"1",
                                                                               }))
    override = forms.BooleanField(required = False, initial = False, widget = forms.HiddenInput)