#-*- coding: utf-8 -*-
from datetime import datetime
import re
import thread

def wywiezSmieci(id, gra, Smieciarka):
    try:
        Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz, (U'Odebranie śmieci z %s ' %id) ))
        cel = gra.Smietniki[int(id)].PunktOdbioru
        Smieciarka.KolejkaZadan.put((thread.start_new_thread, Smieciarka.znajdzTrase, (gra.Plansza[cel[0]][cel[1]],)))
        Smieciarka.KolejkaZadan.put((Smieciarka.oproznijKosz,))
    except KeyError:
        Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz,(U'Nie ma smietnika o id %s' %id)))


def rozpoznaj(user_input, Smieciarka, gra):
    for polecenie in re.split(r' potem | nastepnie | następnie ',user_input):
        if re.findall('odbierz|wsyp|za(l|ł)aduj|pobierz',polecenie,re.IGNORECASE):
            adresyZakresy = re.findall(r'\d+-\d+|od \d+ do \d+',polecenie)
            if adresyZakresy:
                for adresy in adresyZakresy:
                    ad = re.findall(r'\d+',adresy)
                    for i in range(int(ad[0]),int(ad[1])+1):
                        wywiezSmieci(i,gra,Smieciarka)
            else:
                adresy = re.findall(r'\d+', polecenie)
                if adresy:
                    for id in adresy:
                        wywiezSmieci(id,gra,Smieciarka)
                else:
                    Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz, (U'Rozpoznano polecenie odebrania śmieci. Brak kluczowej wartości polecenia.')))
        elif re.findall('godzin(a|ę|e)|czas',polecenie,re.IGNORECASE):
            now = datetime.now()
            Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz, (U'Rozpoznano polecenie wyświetlenia godziny: Aktualna godzina: %s:%s:%s  '% (now.hour, now.minute, now.second))))
        elif re.findall('dat(a|e|ę)|dzie(n|ń)',polecenie,re.IGNORECASE):
            now = datetime.now()
            Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz, (U'Rozpoznano poleceie wyświetlenia daty: Aktualna data: %s/%s/%s '% (now.day, now.month, now.year))))
        elif re.findall('wyj(d(z|ź)|(s|ś)cie)|exit|quit',polecenie,re.IGNORECASE):
            Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz, (U'Wyłączanie')))
            Smieciarka.KolejkaZadan.put((gra.terminate,))
        elif re.findall('pomoc|help|man(ual)',polecenie,re.IGNORECASE):
            print('__Wywołano polecenie pomocy__')
            print('Wpisuj komendy poleceniami tekstowymi')
            print('Jeśli zostaną wpisane dwa lub więcej słowa kluczowe zostanie wywołane polecenie odpowiadające pierwszemu z nich')
            print('Dostępne polecenia:')
            print('1. Wywóz śmieci: odbierz smieci z [numer smietnika] lub np. odbierz smieci z 0-20 lub odbierz smieci od 5 do 25 lub odbierz smieci z 5 6 7 8 i 9 itp.')
            print('2. Wyświetlanie daty, czasu')
            print('3. Wyjście z programu')
            print('4. Opróżnienie śmieciarki: wysyp smieci na smietnisku lub rozładuj smieci na smietnisku')
            print('5. Pomoc')
        elif re.findall('wysyp|roz(l|ł)aduj',user_input,re.IGNORECASE):
            Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz,(U'Rozładowywanie śmieciarki')))
            cel = gra.Wysypisko.PunktDostarczenia
            Smieciarka.KolejkaZadan.put( (thread.start_new_thread, Smieciarka.znajdzTrase, (gra.Plansza[cel[0]][cel[1]], )) )
            Smieciarka.KolejkaZadan.put((Smieciarka.rozladuj,))
        else:
            Smieciarka.KolejkaZadan.put((Smieciarka.odpowiadacz.ustawDopowiedz,(U'Nie rozpoznano polecenia. Użyj polecenia help lub pomoc lub manual  w celu uzyskania pomocy')))
