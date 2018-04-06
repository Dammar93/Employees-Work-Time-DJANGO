from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from faker import Faker
fake = Faker()
from django.conf import settings
import os

def zestaw1(request):
    path = os.path.join(settings.STATIC_DIR, 'logi.txt')
    data = pd.read_csv(path, sep=';', names = ["Data", "Godzina", "Minuty", "Pracownik", "Zdarzenie", "Rejestracja"])
    register_dict = ["Karta identyfikacyjna", "Czytnik linii papilarnych", "Kod dostępu"]
    slownik, slownik2, wszyscy_pracownicy = {}, {}, {0:'Wszyscy Pracownicy'}
    lista = ["-->Wejście", "Wyjście-->", "Wyjście Służbowe"]
    lista2 = data['Pracownik'].unique().tolist()
    wszystkie_rekordy = data['Data'].count()
    zestawienie1_wybory = [wszyscy_pracownicy[0], data['Data'].min(), data['Data'].max(), wszystkie_rekordy]
    wyb = ''
    rekordy = 500

    for key in lista2:
        wszyscy_pracownicy[key] = fake.seed_instance(key).name()


    for key in range(8):
        if key%2 == 0:
            slownik2[key] = lista[0]
        else:
            slownik2[key] = lista[1]
        if key == 5:
            slownik2[key] = lista[2]


    for key in range(3):
        slownik[key] = register_dict[key]

    def mapowanie(id):
        return slownik[id]

    def mapowanie2(id):
        return slownik2[id]

    def mapowanie3(id):
        return wszyscy_pracownicy[id]

    data.Rejestracja = data.Rejestracja.apply(mapowanie)
    data.Zdarzenie = data.Zdarzenie.apply(mapowanie2)
    data.Pracownik = data.Pracownik.apply(mapowanie3)


    if request.method == 'POST':

        zestawienie1_wybory[0] = request.POST.get('wybor_prac')
        zestawienie1_wybory[1] = request.POST.get('data1')
        zestawienie1_wybory[2] = request.POST.get('data2')
        rekordy = request.POST.get('rekordy')


        if zestawienie1_wybory[0] != wszyscy_pracownicy[0]:
            data = data[(data.Pracownik == zestawienie1_wybory[0]) &  (data.Data <= zestawienie1_wybory[2]) & (data.Data >= zestawienie1_wybory[1])]
        else:
            data = data[(data.Data >= zestawienie1_wybory[1]) & (data.Data <= zestawienie1_wybory[2])]


    data = data.iloc[::-1]
    data = data.head(int(rekordy))
    return render(request, 'first_app/index.html', {'data':data,'lista_pracownikow':wszyscy_pracownicy, 'rekordy':rekordy, 'zestaw1':zestawienie1_wybory})
