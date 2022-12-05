from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'remarks') # how other textfield can exist??? I don't get it right now ..
        # we are summing the price base on the transaction ID. 

        