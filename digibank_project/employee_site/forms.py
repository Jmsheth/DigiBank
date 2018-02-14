

class EmpAccActivationSearch(forms.Form):
    f_name = forms.CharField(label="First name:",
                             required=False)
    l_name = forms.CharField(label="Last Name:",
                             required=False)
    u_name = forms.CharField(label="Username",
                             required=False)
    id_num = forms.IntegerField(label="ID Number:",
                                 required=False)


class EmpAccActivation(forms.ModelForm):
    class Meta:
        fields = ["active"]