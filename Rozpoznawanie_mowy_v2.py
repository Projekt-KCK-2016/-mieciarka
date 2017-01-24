#-*- coding: utf-8 -*-

'''
Created on 15.01.2017

@author: kuba
'''

if __name__ == '__main__':
    pass


from datetime import datetime
import re


def apk():
    words_to_check1 = '((s|ś)mieci)|(odpad(y|ki))'
    words_to_check2 = '(godzin(a|ę|e))|(czas)'
    words_to_check3 = '(dat(a|e|ę))|(dzie(n|ń))'
    words_to_check4 = '(wyj(d(z|ź)|(s|ś)cie))|(exit)|(quit)'
    words_to_check5 = '(pomoc)|(help)|(man(ual))'
    words_to_check6 = '(odbierz)|(wsyp)|(za(l|ł)aduj)|(pobierz)'
    words_to_check7 = '(wysyp)|(roz(l|ł)aduj)'
    while True:
        flaga = 0
        user_input = raw_input('Wprowadz polecenie \n')
        
        
        print(re.findall(r"%s"%words_to_check1,user_input,re.IGNORECASE))
        print(re.findall(r"%s"%words_to_check2,user_input,re.IGNORECASE))
        print(re.findall(r"%s"%words_to_check3,user_input,re.IGNORECASE))
        print(re.findall(r"%s"%words_to_check4,user_input,re.IGNORECASE))
        print(re.findall(r"%s"%words_to_check5,user_input,re.IGNORECASE))
        
             
        if not (len(re.findall(r'%s'%words_to_check1,user_input,re.IGNORECASE))<1):
            flaga = 1
        elif not (len(re.findall(r'%s'%words_to_check2,user_input,re.IGNORECASE))<1):
            flaga = 2
        elif not (len(re.findall(r'%s'%words_to_check3,user_input,re.IGNORECASE))<1):
            flaga = 3
        elif not (len(re.findall(r'%s'%words_to_check4,user_input,re.IGNORECASE))<1):
            flaga = 4
        elif not (len(re.findall(r'%s'%words_to_check5,user_input,re.IGNORECASE))<1):
            flaga = 5
        elif not (len(re.findall(r'%s'%words_to_check6,user_input,re.IGNORECASE))<1):
            flaga = 6
        elif not (len(re.findall(r'%s'%words_to_check7,user_input,re.IGNORECASE))<1):
            flaga = 7
        else:
            print('Nie rozpoznano polecenia. \n')
            print('Użyj polecenia help lub pomoc lub manual \n w celu uzyskania pomocy')
            
                
        if flaga == 1:
            string1 = re.findall(r'\w\d', user_input)
            string2 = ''.join(string1)
            if (len(string2) > 1 ):
                print('Rozpoznano polecenie odebrania smieci z %s \n' %string2)
                return string2 
            else:
                print('Rozpoznano polecenie odebrania smieci \n')
                print('Brak kluczowej wartosci polecenia \n')
            
        elif flaga == 2:
            now = datetime.now()
            print('Rozpoznano polecenie wyswietlenia godziny')
            print('Aktualna godzina: %s:%s:%s \n '% (now.hour, now.minute, now.second))
            
        elif flaga == 3:
            now = datetime.now()
            print('Rozpoznano poleceie wyswietlania daty')
            print('Aktualna data: %s/%s/%s '% (now.day, now.month, now.year))          
            
        elif flaga == 4:
            print('Shutdown')
            break
        
        elif flaga == 5:
            print('__Wywołano polecenie pomocy__')
            print('Wpisuj komendy poleceniami tekstowymi')
            print('Jeśli zostaną wpisane dwa lub więcej słowa kluczowe \nzostanie wywołane polecenie odpowiadające pierwszemu z nich')
            print('Dostępne polecenia:')
            print('1. Wywóz śmieci /polecenie [adres wywozu]/')
            print('2. Wyświetlanie daty, czasu')
            print('3. Wyświetlenie statusu śmieciarki !!!UNAVAIABLE!!')
            print('4. Wyjście z programu /exit, quit, wyjście/')
            print('5. Opróżnienie śmieciarki /wysyp, rozładuj/')
            print('6. Opróżnienie kosza /odbierz, pobierz, załaduj, wsyp/')
            print('7. Pomoc /help, manual, pomoc/')
            
        elif flaga == 6:
            print('Opróżnianie kosza')
            #Smieciarka.oproznijKosz()
        
        elif flaga == 7:
            print('Rozładowywanie śmieciarki')
            #Smieciarka.rozladuj()
                                    
def main():

        
        print(apk())
        quit()
        
main()