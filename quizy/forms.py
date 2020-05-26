from django import forms
from .models import *
from django.forms import ModelChoiceField
class Nazwa(forms.ModelForm):
    haslo = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Uzytkownicy
        fields = [
            'nazwa',
            'haslo'
        ]
#
class WyborOdpowiedziForm(forms.ModelForm):    #Odpowiedzi.objects.filter(pytanie='pytanie_id')
    class Meta:
      model = WyborOdpowiedzi
      fields = ['Odpowiedz']

class Login(forms.ModelForm):
    haslo = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Uzytkownicy
        fields = [
            'nazwa',
            'haslo'
        ]

class Wyniki(forms.ModelForm):
    class Meta:
        model = WynikiModel
        fields = ['wynik']

class Fooform(forms.Form):
    btn = forms.CharField()


    #https://stackoverflow.com/questions/52602663/how-do-i-add-input-type-button-as-a-formfield-in-django # PRZYCISKI W DJANGO