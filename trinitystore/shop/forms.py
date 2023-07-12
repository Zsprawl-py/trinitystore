from django import forms
from .models import Product


# class ChoiceProduct(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ('name',)
#         widgets = {
#             'name' :
#         }


class ChoiceProduct(forms.Form):
    pass
