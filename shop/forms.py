from django import forms
from .models import Coupon


class SearchField(forms.Form):
    query = forms.CharField(widget = forms.TextInput(attrs={"class":'form-control rounded-0 rounded-end-3','id':'searchField', 'placeholder':"Search..."}),required=False)
    

class CouponField(forms.Form):
    code = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','aria-describedby':"button-addon1",'placeholder':'Code...'}))
