from django import forms
from customer_site.models import Customer

class EmpAccActivationSearch(forms.Form):
    f_name = forms.CharField(label="First name:",
                             required=False)
    l_name = forms.CharField(label="Last Name:",
                             required=False)
    u_name = forms.CharField(label="Username",
                             required=False)
    id_num = forms.IntegerField(label="ID Number:",
                                 required=False)

class NewCustomer(forms.Form):
    class Meta:
        model = Customer
        fields = ('firstName','middleName','lastName','address','city','state','country','zipCode','phoneNumber','kycId','idNumber','userid',
                  'password')