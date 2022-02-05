from django import forms
from config.validators import PhoneValidator
from config.validators2 import PhoneValidatorTest
from django.core.validators import MinLengthValidator, EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from .models import UserModel

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label=False, widget=forms.TextInput(attrs={'id': 'username'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'id': "password"}), required=True,
                               validators=[MinLengthValidator(6)], label=False)


class RegistrationForm(forms.Form):
    phone = forms.CharField(max_length=14, required=True, validators=[PhoneValidator()],
                            widget=forms.TextInput(attrs={'placeholder': '998941234567'}), label=False)
    avatar = forms.ImageField(label=False, required=False)
    username = forms.CharField(max_length=20, required=True,
                               validators=[UnicodeUsernameValidator()], label=False)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True,
                               validators=[MinLengthValidator(6)], label=False)
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True,
                              validators=[MinLengthValidator(6)], label=False)

    def clean_username(self):
        if UserModel.objects.filter(username=self.cleaned_data.get('username')).exists():
            raise ValidationError("Ushbu username mavjud")

        return self.cleaned_data["username"]

    def clean_phone(self):
        if UserModel.objects.filter(phone=self.cleaned_data.get('phone')).exists():
            raise ValidationError("Ushbu telefon raqam band")

        return self.cleaned_data["phone"]

    def clean_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
                raise ValidationError("Parollar bir xil emas !")

        return self.cleaned_data['confirm']

class ForgotPassword(forms.Form):
    phone = forms.CharField(max_length=16, label=False,
                            widget=forms.TextInput(attrs=({"class": "rounded-15", 'placeholder': '998971234567',
                                                           'id': 'phone_number'})),
                            validators=[PhoneValidator(), PhoneValidatorTest()], required=True)
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs=({"class": "rounded-15",
                                                                                     'id': "new_password"})),
                                   required=True, validators=[MinLengthValidator(6)], label=False)
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs=({"class": "rounded-15", "id": "confirm"})),
                              required=True, validators=[MinLengthValidator(6)], label=False)

    def clean_confirm(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm']:
            raise ValidationError(_("Parollar bir xil emas !"))

        return self.cleaned_data['confirm']


class GetCodeForm(forms.Form):
    code = forms.IntegerField(max_value=6, label=False,
                              widget=forms.TextInput(attrs=({"class": "rounded-15", 'placeholder': 'Kodni kiriting',
                                                             'id': "code"})), required=True)