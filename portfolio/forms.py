from django.forms import ModelForm
from .models import Currencies


class MyModelForm(ModelForm):
    class Meta:
        model = Currencies
        fields = ['currency_name']
