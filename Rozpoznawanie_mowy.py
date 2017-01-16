'''
Created on 15.01.2017

@author: kuba
'''
import string

if __name__ == '__main__':
    pass

#-*- coding: utf-8 -*-

from datetime import datetime
import re




def apk():
    words_to_check1 = ['smieci' , 'odpady']
    words_to_check2 = ['godzina' , 'godzine' , '[czas]']
    words_to_check3 = ['date' , 'data' , 'dzien']
    words_to_check4 = ['wyjdz', 'wyjscie', 'exit' , 'quit']
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
                return string2 #główna musi sama sobie wywoływać kiedy tego potrzebuje, całe moje 
            else:
                print('Rozpoznano polecenie odebrania smieci \n')
                print('Brak kluczowej wartosci polecenia \n')
            
        elif flaga == 2:
            now = datetime.now()
            print('Rozpoznano polecenie wyswietlenia godziny')
            print('Aktualna godzina: %s:%s:%s \n '% (now.hour, now.minute, now.second))
        
        elif flaga == 3:
            now = datetime.now()
            print('Aktualna data: ')          
            print('%s/%s/%s' % (now.day, now.month, now.year))
            
        elif flaga == 4:
            print('Shutdown')
            break
            #
            #
            #
            #zwracać wartość, żeby główna funkcja sama odpaliła sys.exit
            #lub robić to od razu tutaj, do dogadania
            #
            #
            #
                
            
            
                        
                    
                    
def main():

        
        apk()
        quit()
        
main()