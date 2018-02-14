from django import forms
from core_files.models import Account
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.contrib.admin.widgets import AdminDateWidget


class userAccountSummary(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('owner', 'accountNum', 'acntType')


class userTransactionReport(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('owner','accountNum', 'acntType',)


class userFundsTransfer(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('accountNum', 'routingNum','owner')
