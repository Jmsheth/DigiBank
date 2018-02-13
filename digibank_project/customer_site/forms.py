from django import forms
from .models import Account
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

class userAccountSummary(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('accountNum','acntType')
        dateFrom = DateField(widget=AdminDateWidget)
        dateTo = DateField(widget=AdminDateWidget)

class userTransactionReport(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('accountNum', 'acntType')
        dateFrom = DateField(widget=AdminDateWidget)
        dateTo = DateField(widget=AdminDateWidget)

class userFundstransfer(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('accountNum', 'routingNum')
