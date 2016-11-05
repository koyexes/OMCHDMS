from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from django.utils.crypto import get_random_string
from models import state, hmo, patient, drug

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length = 20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class PatientForm(forms.Form):
    attributes = {'class' : 'form-control', 'required' : 'True'}
    surname = forms.CharField(max_length=15,  widget= forms.TextInput(attrs= attributes))
    firstname = forms.CharField(max_length= 15, widget= forms.TextInput(attrs= attributes))
    othername = forms.CharField(max_length= 15, widget= forms.TextInput(attrs= {'class' : 'form-control'}))
    cardNo = forms.CharField(max_length=15,  widget= forms.TextInput(attrs= attributes))
    gender = forms.ChoiceField(choices= (("M", "Male"), ("F", "Female")), initial= "M", widget= forms.Select(attrs=attributes))
    mobileNo = forms.CharField( widget= forms.TextInput(attrs= attributes))
    address = forms.CharField( widget= forms.TextInput(attrs= attributes))
    origin = forms.ModelChoiceField(widget=forms.Select(attrs=attributes), queryset= state.objects.order_by("state_name"), empty_label="Select a State")
    hmo = forms.ModelChoiceField( widget=forms.Select(attrs=attributes), queryset= hmo.objects.order_by("name"), empty_label= "Select an HMO")

    def __init__ (self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PatientForm, self).__init__(*args, **kwargs)

    def __str__(self):
        data = self.cleaned_data
        return ("%s %s with card number: %s has been created" % ((data['surname']).upper(), (data['firstname']).upper(), data['cardNo']))


    def save (self):
        data = self.cleaned_data
        new_patient = patient(surname = data['surname'], firstname = data['firstname'], othernames = data['othername'],                              card_no = data['cardNo'], gender = data['gender'], phone_number = data['mobileNo'],                                  address = data['address'], hmo = data['hmo'], added_by = self.user,
                              origin = data['origin'])
        try:
            new_patient.save()
            return [True]
        except Exception:
            return [False, "%s %s with card number: %s wasn't created" % ((data['surname']).upper(), (data['firstname']).upper(), data['cardNo'])]

class DrugForm(forms.Form):
    attributes = {'class' : 'form-control', 'required' : 'True'}
    drug_name = forms.CharField(max_length = 15, required = True, widget = forms.TextInput(attrs = attributes))
    drug_code = forms.CharField(max_length = 15, required = True, widget = forms.TextInput(attrs = attributes))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DrugForm, self).__init__(*args, **kwargs)

    def __str__(self):
        data = self.cleaned_data
        return "%s with Drug Code: %s has been created" % ((data['drug_name']).upper(), (data['drug_code']).upper())

    def save(self):
        data = self.cleaned_data
        new_drug = drug(drug_name = data['drug_name'], drug_code = data['drug_code'], added_by = self.user)
        try:
            new_drug.save()
            return [True, "%s with Drug Code: %s wasn't created" % ((data['drug_name']).upper(), (data['drug_code']).upper())]

        except Exception:
            return [False, "%s with Drug Code: %s wasn't created" % ((data['drug_name']).upper(), (data['drug_code']).upper()) ]

class HmoForm(forms.Form):
    attributes = {'class': 'form-control'}
    name = forms.CharField(max_length = 25, required = True, widget = forms.TextInput(attrs = attributes))
    mobile = forms.CharField(max_length = 15, required = True, widget = forms.TextInput(attrs = attributes))
    email = forms.EmailField(widget = forms.EmailInput(attrs = attributes))
    address = forms.CharField(required = True, widget = forms.TextInput(attrs = attributes))
    hmo_status = forms.ChoiceField(choices = (("1", "Active"), ("0", "Inactive")), initial = "1",
                                   widget = forms.Select(attrs = attributes))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(HmoForm, self).__init__(*args, **kwargs)

    def __str__(self):
        data = self.cleaned_data
        return "%s has been created" % (data['name'])

    def save(self):
        data = self.cleaned_data
        new_hmo  = hmo(name = data['name'], mobile = data['mobile'], email = data['email'], address = data[
            'address'], hmo_status = int(data['hmo_status']), added_by = self.user)
        try:
            new_hmo.save()
            return [True]

        except Exception:
            return [False, "%s wasn't created" % ((data['name']).upper()) ]

class ChangePassword(forms.Form):
    currentPassword = forms.CharField(required = True, max_length = 128, widget = forms.PasswordInput(attrs = {'id' : 'current-password', 'class' : 'form-control'}))
    newPassword = forms.CharField(required = True, max_length = 128, widget = forms.PasswordInput(attrs = {'id' : 'new-password', 'class' : 'form-control'}))
    confirmNewPassword = forms.CharField(required = True, max_length = 128, widget = forms.PasswordInput(attrs = {
        'id' : 'confirm-password', 'class' : 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePassword, self).__init__(*args, **kwargs)

    def __str__(self):
        data = self.cleaned_data
        return "%s, your password has been changed successfully" % (self.user.username)

    def save(self):
        data = self.cleaned_data
        user = User.objects.get(id = self.user.id)
        user.password = hashers.make_password(data['newPassword'], get_random_string(32))
        try:
            user.save()
            return True

        except Exception:
            return  False



