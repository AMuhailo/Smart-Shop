from django import forms
from .models import Coupon

class CouponField(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','aria-describedby':"button-addon1",'placeholder':'Code...'}))
