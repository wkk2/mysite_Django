from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    name = forms.CharField(label='username',max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password',max_length=32,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='validation')
 #   email = forms.EmailField()
 #   sex = forms.ChoiceField(('male','female'))

class RegisterForm(forms.Form):
    gender = (('male','男'),('female','女'))
    name = forms.CharField(label='username',max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password',max_length=32,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Check password again',max_length=32,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label='sex',choices=gender)
    captcha = CaptchaField(label='validation')
