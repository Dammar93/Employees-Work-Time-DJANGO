from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from faker import Faker
fake = Faker()
import calendar
from datetime import datetime
from django.conf import settings
import os

def zestaw2(request):
    path = os.path.join(settings.STATIC_DIR, 'logi.txt')
    global data
    data = pd.read_csv(path, sep=';', names = ["Data", "Godzina", "Minuty", "Pracownik","Zdarzenie", "Rejestracja"])
    slownik_mies, slownik3 = {}, {}
    lista_map_mies = ['Styczeń','Luty','Marzec','Kwiecień','Maj','Czerwiec','Lipiec','Sierpień','Wrzesień','Październik','Listopad','Grudzień']
    lista_rok = sorted(pd.DatetimeIndex(data['Data']).year.unique().tolist())
    lista_mies = sorted(pd.DatetimeIndex(data['Data']).month.unique().tolist())
    lista2 = data['Pracownik'].unique().tolist()

    for key in lista2:
        slownik3[key] = fake.seed_instance(key).name()

    zestawienie1_wybory = [slownik3, slownik_mies, lista_rok, slownik3[lista2[0]], min(lista_mies), min(lista_rok)]
    global dni_miesiaca
    dni_miesiaca = calendar.monthcalendar(int(zestawienie1_wybory[5]), int(zestawienie1_wybory[4]))
    przepracowany_czas = 0
    data['Data'] = pd.to_datetime(data['Data'])

    for key in lista2:
        slownik3[key] = fake.seed_instance(key).name()


    def glowne_obliczenie_godzin():
        if request.method == 'POST':
            global dni_miesiaca
            zestawienie1_wybory[3] = request.POST.get('wybor_prac')
            zestawienie1_wybory[4] = request.POST.get('wybor_mies')
            zestawienie1_wybory[5] = request.POST.get('wybor_rok')
            dni_miesiaca = calendar.monthcalendar(int(zestawienie1_wybory[5]), int(zestawienie1_wybory[4]))

        global data
        data = data[(data.Pracownik == zestawienie1_wybory[3]) & (data['Data'].dt.year == datetime(int(zestawienie1_wybory[5]), 1, 1).year) & (data['Data'].dt.month == datetime(2000, int(zestawienie1_wybory[4]), 1).month)]
        data_wejscia = 0
        data_wyjscia = 0
        przepracowany_czas = 0
        przepracowane_godziny = {}
        dzien = 0

        for tygodnie in dni_miesiaca:
            for dni in tygodnie:
                przepracowane_godziny[dni] = 0


        for index, row in data.iterrows():
            if row['Zdarzenie'] % 2 == 0:

                if row[0].day != dzien:
                    data_wejscia = 0

                if data_wejscia == 0:
                    data_wejscia = row[0] + pd.Timedelta(hours = row[1], minutes = row[2])
                    dzien = row[0].day
            else:
                if data_wejscia != 0:
                    data_wyjscia = row[0] + pd.Timedelta(hours = row[1], minutes = row[2])
                    przepracowany_czas += pd.Timedelta(data_wyjscia - data_wejscia).total_seconds()
                    przepracowany_dzien = pd.Timedelta(data_wyjscia - data_wejscia).total_seconds()
                    przepracowane_godziny[row[0].day] += przepracowany_dzien
                    data_wejscia = 0


        for key, value in przepracowane_godziny.items():
            przepracowane_godziny[key] = "{0[0]:.0f}:{0[1]:02.0f}".format(convert_seconds(value))


        przepracowany_czas = "{0[0]:.0f}:{0[1]:02.0f}".format(convert_seconds(przepracowany_czas))
        return render(request, 'first_app/zestaw2.html', {'data':data,'zestaw1':zestawienie1_wybory, 'dni_miesiaca':dni_miesiaca, 'czaspracy':przepracowany_czas, 'godzinydzien':przepracowane_godziny})


    def convert_seconds(seconds):
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        return hours, minutes

    def mapowanie3(id):
        return slownik3[id]

    for i in range(len(lista_mies)):
        slownik_mies[i+1] = lista_map_mies[i]


    data.Pracownik = data.Pracownik.apply(mapowanie3)
    return glowne_obliczenie_godzin()
