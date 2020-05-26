from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Pytania(models.Model):
    tresc = models.CharField(max_length=150)
    tworca = models.ForeignKey(User, null=True, blank=False, default='kacper', on_delete=models.CASCADE)
    def __str__(self):
        return self.tresc

    def get_queryset(self):
        return Pytania.objects.all()


class Odpowiedzi(models.Model):
    pytanie = models.ForeignKey(Pytania, on_delete=models.CASCADE)
    tresc = models.TextField()
    prawda = models.BooleanField(default=False)
    def __str__(self):
        return self.tresc

class Uzytkownicy(models.Model):
    nazwa = models.CharField(max_length=30)
    haslo = models.CharField(max_length=30)
    def __str__(self):
        return self.nazwa

class WyborOdpowiedzi(models.Model):
    uzytkownik = models.ForeignKey(Uzytkownicy, null=True, on_delete=models.CASCADE)
    pytanie = models.ForeignKey(Pytania, null=True,  on_delete=models.CASCADE)
    Odpowiedz = models.CharField(null=True,max_length=50)



class WynikiModel(models.Model):
    uzytkownik = models.ForeignKey(Uzytkownicy, null=True, on_delete=models.CASCADE)
    wynik=models.CharField(null=True,max_length=50)

    def __str__(self):
        return self.wynik


