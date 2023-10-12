from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import *
from activities.models import *
import secrets
import string


class registerForm(forms.Form):

    username = forms.CharField(max_length=20,label="Kullanıcı İsmi")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola Tekrarı",widget=forms.PasswordInput)

    name = forms.CharField(label="İsminiz:")

    email = forms.EmailField(label="email Adresiniz:")
    phone = forms.IntegerField(label="Telefon Numaranız:")

    gender = forms.ChoiceField(
        choices=[('Kadın','Kadın'),('Erkek','Erkek'),('Diğer','Diğer')]
    )

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        name = self.cleaned_data.get("name")

        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")
        gender = self.cleaned_data.get("gender")

        if str(username) in str(usercore.objects.all()):
            raise forms.ValidationError("Bu kullanıcı adı daha önceden alındı.")
            
        for who in usercore.objects.all():
            if str(who.email) == str(email):
                raise forms.ValidationError("Bu e-posta adresi daha önceden alındı.")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")
            
        for who in usercore.objects.all():
            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır")

        if len(phone) != 12:
            raise forms.ValidationError("Telefon numaranızı, 905xxxxxxxxx formatında, 12 haneli olarak giriniz.")
        
        value = {
            "username" : username,
            "password" : password,
            "name": name,
            "email": email,
            "phone": phone,
            "gender": gender,
        }

        return value

class loginForm(forms.Form):

    username = forms.CharField(max_length=20,label="Kullanıcı İsmi")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)

class updateForm(forms.Form):
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput,required=False)
    email = forms.EmailField(label="email Adresiniz:",required=False)
    phone = forms.IntegerField(label="Telefon Numaranız:",required=False)
    pic1 = forms.ImageField(label="Profil Fotoğrafı",required=False)

    def clean(self):

        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")
        pic1 = self.cleaned_data.get("pic1")
            
        for who in usercore.objects.all():
            if str(who.email) == str(email):
                raise forms.ValidationError("Bu e-posta adresi daha önceden alındı.")
            
        for who in usercore.objects.all():
            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır")

        if len(phone) != 12:
            raise forms.ValidationError("Telefon numaranızı, 905xxxxxxxxx formatında, 12 haneli olarak giriniz.")
        
        value = {
            "password" : password,
            "email": email,
            "phone": phone,
            "pic1":pic1,
        }

        return value