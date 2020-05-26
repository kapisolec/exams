from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, loader, redirect
from django.urls import reverse
from quizy.models import *
from .forms import *

from django.template.context_processors import request

def start(request):
    try: request.session['username']
    except KeyError: request.session['username']=None
    if request.session['username'] is not None:
        context= {'username':request.session['username']}
    else:
        context={}
    return render(request, "quizy/index.html",context )


def login(request): #logowanie
    form = Login(request.POST or None)
    error = "Podałeś złe dane, spróbuj ponownie"
    if form.is_valid():
        if Uzytkownicy.objects.filter(nazwa=form.cleaned_data['nazwa']).exists():
            request.session['username'] = form.cleaned_data['nazwa']
            print(request.session['username'])
            request.session['wynik'] = 0
            return redirect("welcome")
        else:
            context = {
                'form': form,
                'error': error
            }
            return render(request, "quizy/login.html", context)
    else:
        context = {
            'form':form
        }
        return render(request, "quizy/login.html", context)

def homeView(request, pytania_id=1): #rejestracja sie
    form = Nazwa(request.POST or None)
    error1 = "W bazie danych jest już taki użytkownik"
    error2 = "Hasło musi mieć więcej niż 4 znaki"
    if form.is_valid():
        if Uzytkownicy.objects.filter(nazwa=form.cleaned_data['nazwa']).exists():
            context = {
                'form':form,
                'error':error1
            }
            return render(request, "quizy/nameCreateView.html", context)
        elif len(form.cleaned_data['haslo']) < 5:
            context = {
                'form':form,
                'error':error2
            }
            return render(request, "quizy/nameCreateView.html", context)

        else:
            username = form.cleaned_data['nazwa']
            request.session['username'] = username
            form.save()
            print(request.session['username'])
            request.session['wynik'] = 0
            return redirect("detail", pytania_id)
           # return redirect("welcome")
    else:
        context = {
            'form': form
        }
        return render(request, "quizy/nameCreateView.html", context)






def detail(request, pytania_id):
    username = request.session['username']  ##################################
    if request.session['username'] == None:
        return redirect("login")
    else:
        form=WyborOdpowiedziForm(request.POST or None)
        ListaOdp=[]
        odp_id=pytania_id
        #SESJA
        print(username)
        pytanie = Pytania.objects.get(id=pytania_id)
        q = Odpowiedzi.objects.filter(pytanie_id=pytania_id).all()
        qList = list(q)
        for i in qList:
            ListaOdp.append(str(i))

        context = {
            'pytaniaObjCount':Pytania.objects.count(),
            'pytania_id':pytania_id,
            'username':username,
            'form':form,
            'pytanie': pytanie,
            'odp': ListaOdp,
        }
       # print(i)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.uzytkownik = Uzytkownicy.objects.get(nazwa=username) #uzytkownik zostaje wpisany ze zmiennej sesyjnj
            obj.pytanie = Pytania.objects.get(pk=pytania_id)
            obj.save()

            odp = Odpowiedzi.objects.filter(pytanie=pytania_id, prawda=True)
            odp = str(odp.get())
            if odp.lower() == form.cleaned_data['Odpowiedz'].lower():
                request.session['wynik'] += 1
            pytania_id = (int(pytania_id) + 1)

            if pytania_id <= Pytania.objects.count():

                return redirect("detail", pytania_id)
            else:

                return redirect("wyniki")
        else:
            return render(request, 'quizy/detail.html', context)





def wyniki(request):
    if request.session['username'] == None:
        return redirect("login")
    else:
        max = Pytania.objects.all().count()
        wynik = request.session['wynik']
        procent = str(round(float(wynik/max),1)*100)+"%"
        print("DEBUG WYNIKU W wyniki -> ",wynik)
        username = request.session['username']
        obj = WynikiModel.objects.create(wynik=procent, uzytkownik=Uzytkownicy.objects.get(nazwa=username))
        obj.save()
        context={
            'username':username,
            'wynik':procent,
        }
    return render(request, 'quizy/wyniki.html', context)



def wyswietlWynik(request,pytania_id=1):
    if WynikiModel.objects.filter(uzytkownik=Uzytkownicy.objects.get(nazwa=request.session['username']).id).count()<1:
        return render(request, 'quizy/brakWynikow.html', {})
    else:
        if request.session['username'] == None:
            return redirect("login")
        else:
            tablicaWynikow =[]
            form = Fooform(request.POST or None)
            username = request.session['username']
         #   print("NAZWA UZYTKOWNIKA ->",username)# debug
            uzytkownikId=Uzytkownicy.objects.get(nazwa=username).id
            #print("ID UZYTKOWNIKA ->", uzytkownikId)
            allWyniki =  list(WynikiModel.objects.filter(uzytkownik=uzytkownikId))
            if len(allWyniki) > 0:
                for i in allWyniki:
                    tablicaWynikow.append(str(i))
             #  print("TABLICA WYNIKOW ->", allWyniki)
                latest = tablicaWynikow[-1]
                context = {
                    'tablicaWynikow':tablicaWynikow,
                    'latest':latest,
                    'username':username
                }
                return render(request, 'quizy/twojeWyniki.html', context)


def logout(request):
    if request.session['username'] == None:
        return redirect('login')
    else:
        request.session['username'] = None
        return render(request,'quizy/logout.html',{})

def about(request):
    if request.session['username'] == None:
        return render(request,'quizy/about.html',{'username':None})
    else:
        return render(request,'quizy/about.html',{'username':request.session['username']})