#-*- coding: utf-8 -*-

'''
Created on 15.01.2017

@author: kuba
'''
import string

if __name__ == '__main__':
    pass


from datetime import datetime
import re


def apk():
    words_to_check1 = ['smieci' , 'odpady', 'śmieci']
    words_to_check2 = ['godzina' , 'godzine' , 'czas', 'godzinę']            #te pierdoły beda zmienione na reguly regexu
    words_to_check3 = ['date' , 'data' , 'dzien', 'datę', 'dzień']
    words_to_check4 = ['wyjdz' , 'wyjscie' , 'exit' , 'quit', 'wyjdź', 'wyjście']
    while True:
        flaga = 0
        user_input = raw_input('Wprowadz polecenie \n')
            
        if any(word in user_input for word in words_to_check1):
            flaga = 1
        elif any(word in user_input for word in words_to_check2):
            flaga = 2
        elif any(word in user_input for word in words_to_check3):
            flaga = 3
        elif any(word in user_input for word in words_to_check4):
            flaga = 4
        else:
            print('Nie rozpoznano polecenia. \n')
            
                
        if flaga == 1:
            string1 = re.findall(r'\w\d', user_input)
            string2 = ''.join(string1)
            if (len(string2) > 1 ):
                print('Rozpoznano polecenie odebrania smieci z %s \n' %string2)
                return string2 #glowna musi sama sobie wywolywac kiedy tego potrzebuje, cale moje 
            else:
                print('Rozpoznano polecenie odebrania smieci \n')
                print('Brak kluczowej wartosci polecenia \n')
            
        elif flaga == 2:
            now = datetime.now()
            print('Rozpoznano polecenie wyswietlenia godziny')
            print('Aktualna godzina: %s:%s:%s \n '% (now.hour, now.minute, now.second))
            #jak sie pyta tylko o date/godzine czyli jakies pierdoly to dziala w kolko
            #a jak kaze wywiezc smieci to sie wylacza zeby smieciarka mogla zrobic swoje
        
        elif flaga == 3:
            now = datetime.now()
            print('Rozpoznano poleceie wyswietlania daty')
            print('Aktualna data: %s/%s/%s '% (now.day, now.month, now.year))          
            
        elif flaga == 4:
            print('Shutdown')
            break
            #
            #
            #
            #zwracac wartosc, zeby glowna funkcja sama odpalila sys.exit
            #lub robic to od razu tutaj, do dogadania
            #
            #
            #
                
            
            
                        
                    
                    
def main():

        
        print(apk())
        quit()
        
main()