#-*- coding: utf-8 -*-
import random, pygame, sys
from pygame.locals import *
from Rozpoznawanie_mowy import rozpoznaj
import pygame_textinput
import py_compile
import time
import heapq
import thread
import random
import Queue

import threading

from Tkinter import Tk

py_compile.compile("main.py")

FPS = 60
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

CELLCOUNTX = WINDOWWIDTH/CELLSIZE
CELLCOUNTY = WINDOWHEIGHT/CELLSIZE

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)
ORANGE    = (255, 165,   0)
BLUE      = (  0,   0, 255)
BROWN     = (139,   69, 19)
BGCOLOR = BLACK

def main():
    gra = Gra()

    while True:
        gra.menu()

class Gra:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Smieciarka')
        self.Plansza = [[None for y in range(CELLCOUNTY)] for x in range(CELLCOUNTX)]
        for x in range(0, CELLCOUNTX):
            for y in range(0, CELLCOUNTY):
                self.Plansza[x][y] = Punkt(x,y)
        self.Elementy = []
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.BASICFONT = pygame.font.SysFont("monospace", 15)
        self.Smietniki = {}
        self.Wysypisko = None

    def get(self):
        return self

    def terminate(self):
        pygame.quit()
        sys.exit()

    def wczytaj(self,f):
        obiekt = ""
        x = ""
        y = ""
        i = 0
        while f[i] != ',':
            obiekt += f[i]
            i += 1
        i+=1
        while f[i] != ',':
            x += f[i]
            i += 1
        i+=1
        while f[i] != '\n':
            y += f[i]
            i += 1
    
        return ( obiekt, int(x), int(y) )

    def wczytajPoziom(self,nazwa):
        try:
            Poziom = open(nazwa, 'r')
        except IOError:
            self.wczytajPoziom(self.zapytanie("Nie ma takiego pliku! Podaj nazwe poziomu, ktory chcesz wczytac.") + ".txt")
            return

        self.Elementy = []
        for x in range(0, CELLCOUNTX):
            for y in range(0, CELLCOUNTY):
                self.Plansza[x][y] = Punkt(x,y)

        ID = 0
        for line in Poziom:
            Obiekt = self.wczytaj(line)
            if Obiekt[0] == "sa":
                self.Plansza[Obiekt[1]][Obiekt[2]].walkable = False
                self.Plansza[Obiekt[1]][Obiekt[2]].obiekt = Smieciarka(Obiekt[1],Obiekt[2],self.get())
                self.Elementy.append(self.Plansza[Obiekt[1]][Obiekt[2]].obiekt)
            elif Obiekt[0] == "sm" or Obiekt[0] == "sp" or Obiekt[0] == "sk" or Obiekt[0] == "sl":
                self.Plansza[Obiekt[1]][Obiekt[2]].walkable = False
                if Obiekt[0] == "sm":
                    self.Plansza[Obiekt[1]][Obiekt[2]].obiekt = SmietnikMakulatura(Obiekt[1],Obiekt[2],self.get(),ID)
                elif Obiekt[0] == "sp":
                    self.Plansza[Obiekt[1]][Obiekt[2]].obiekt = SmietnikPlastik(Obiekt[1],Obiekt[2],self.get(),ID)
                elif Obiekt[0] == "sk":
                    self.Plansza[Obiekt[1]][Obiekt[2]].obiekt = SmietnikSzklo(Obiekt[1],Obiekt[2],self.get(),ID)
                elif Obiekt[0] == "sl":
                    self.Plansza[Obiekt[1]][Obiekt[2]].obiekt = SmietnikAluminium(Obiekt[1],Obiekt[2],self.get(),ID)
                self.Elementy.append(self.Plansza[Obiekt[1]][Obiekt[2]].obiekt)
                self.Smietniki[ID] = self.Plansza[Obiekt[1]][Obiekt[2]].obiekt
                ID += 1
            elif Obiekt[0] == "sc":
                self.Plansza[Obiekt[1]][Obiekt[2]].walkable = False
                self.Plansza[Obiekt[1]][Obiekt[2]].obiekt = Sciana(Obiekt[1],Obiekt[2],self.get())
                self.Elementy.append(self.Plansza[Obiekt[1]][Obiekt[2]].obiekt)
            elif Obiekt[0] == "wy":
                self.Plansza[Obiekt[1]][Obiekt[2]].walkable = False
                self.Plansza[Obiekt[1]][Obiekt[2]].obiekt = Wysypisko(Obiekt[1],Obiekt[2],self.get())
                self.Elementy.append(self.Plansza[Obiekt[1]][Obiekt[2]].obiekt)

    def zapisz(self, nazwa):
        f = open(nazwa, 'w')
        for y in range(0,CELLCOUNTY):
            for x in range(0,CELLCOUNTX):
                if self.Plansza[x][y].obiekt != None:
                    f.write(self.Plansza[x][y].obiekt.nazwa + "," + str(self.Plansza[x][y].obiekt.Poz[0]) + "," + str(self.Plansza[x][y].obiekt.Poz[1]) + "\n")

    def menu(self):
        myszka = 0, 0
        srodek = CELLCOUNTX/2-8
        Przyciski = [Przycisk(srodek,1,"Edytor",self.edytor,16,5,self.get()), Przycisk(srodek,7,"Gra",self.graj,16,5,self.get()), Przycisk(srodek,13,"Wyjdz",self.terminate,16,5,self.get())]
        while True:
            MouseClicked = False
            events = pygame.event.get()
        
            for event in events:
                if event.type == QUIT:
                    self.terminate()
                elif event.type == MOUSEBUTTONUP:
                    MouseClicked = True
        
            self.DISPLAYSURF.fill(BGCOLOR)

            for i in Przyciski:
                i.rysuj()
                if MouseClicked == True:
                    if i.isClicked():
                        i.funkcja()
        
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

    def graj(self):

        myszka = 0, 0
        textinput = pygame_textinput.TextInput()
        textinput.set_text_color(RED)
        textinput.set_cursor_color(RED)

        self.wczytajPoziom(self.zapytanie("Podaj nazwe poziomu, ktory chcesz wczytac.") + ".txt")
        Smieciarka = None
        for i in self.Elementy:
            if i.nazwa == "sa":
                Smieciarka = i
                self.Elementy.remove(i)

        for i in self.Elementy:
            if i.nazwa == "wy":
                self.Wysypisko = i

        while True:
            MouseClicked = False
            events = pygame.event.get()
        
            for event in events:
                if event.type == QUIT:
                    self.terminate()
                elif event.type == MOUSEMOTION:
                    myszka = event.pos
                elif event.type == MOUSEBUTTONUP:
                    MouseClicked = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_SPACE:
                        pass

            if textinput.update(events):
                print(textinput.get_text())
                rozpoznaj(textinput.get_text().encode('utf-8'), Smieciarka.get(), self.get())
                textinput.input_string = ""
                textinput.cursor_position = 0;
        
            self.DISPLAYSURF.fill(BGCOLOR)
            self.rysujSiatke()
            Ticks = pygame.time.get_ticks()

            if MouseClicked:
                if self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt == None:
                    #thread.start_new_thread( Smieciarka.znajdzTrase, ( self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE], ) )
                    pass
        
            for i in self.Elementy:
                i.tick(Ticks)
                i.rysuj()

            Smieciarka.tick(Ticks)
            Smieciarka.rysuj()

            self.DISPLAYSURF.blit(textinput.get_surface(), (15, 15))
        
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)
    
    def edytor(self):
        myszka = 0, 0
        smieciarkaNaPlanszy = False

        wybor = 0
        ID = 0

        self.wczytajPoziom(self.zapytanie("Podaj nazwe poziomu, ktory chcesz edytowac.") + ".txt")

        for i in self.Elementy:
            if i.nazwa == "sa":
                smieciarkaNaPlanszy = True

        obiekt = Smieciarka(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get())
    
        while True:
            leftMouseClicked = False
            rightMouseClicked = False
            events = pygame.event.get()
        
            for event in events:
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if event.key == K_s:
                        self.zapisz(self.zapytanie("Podaj nazwe poziomu, pod ktora chcesz go zapisac.") + ".txt")
                    if event.key == K_SPACE:
                        wybor += 1
                        if wybor == 7:
                            wybor = 0

                        if wybor == 0:
                            obiekt = Smieciarka(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get())
                            smieciarkaNaPlanszy = True
                        elif wybor == 1:
                            obiekt = SmietnikMakulatura(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                            obiekt.PunktOdbioru = (-1,-1)
                        elif wybor == 2:
                            obiekt = SmietnikPlastik(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                            obiekt.PunktOdbioru = (-1,-1)
                        elif wybor == 3:
                            obiekt = SmietnikSzklo(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                            obiekt.PunktOdbioru = (-1,-1)
                        elif wybor == 4:
                            obiekt = SmietnikAluminium(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                            obiekt.PunktOdbioru = (-1,-1)
                        elif wybor == 5:
                            obiekt = Sciana(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get())
                        elif wybor == 6:
                            obiekt = Wysypisko(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get())
                elif event.type == MOUSEMOTION:
                    myszka = event.pos
                elif event.type == MOUSEBUTTONUP:
                    myszka = event.pos
                    if event.button == 1:
                        leftMouseClicked = True
                    elif event.button == 3:
                        rightMouseClicked = True
        
            self.DISPLAYSURF.fill(BGCOLOR)
            self.rysujSiatke()

            if leftMouseClicked == True:
                if self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt == None:
                    if wybor == 0 and not smieciarkaNaPlanszy:
                        a = Smieciarka(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get())
                        self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = a
                        smieciarkaNaPlanszy = True
                    elif wybor == 1:
                        a = SmietnikMakulatura(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                        self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = a
                        ID += 1
                    elif wybor == 2:
                        a = SmietnikPlastik(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                        self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = a
                        ID += 1
                    elif wybor == 3:
                        a = SmietnikSzklo(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                        self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = a
                        ID += 1
                    elif wybor == 4:
                        a = SmietnikAluminium(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get(),ID)
                        self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = a
                        ID += 1
                    elif wybor == 5:
                        a = Sciana(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get())
                        self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = a
                    elif wybor == 6:
                        a = Wysypisko(myszka[0]/CELLSIZE,myszka[1]/CELLSIZE,self.get())
                        self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = a
                    try:
                        self.Elementy.append(a)
                    except UnboundLocalError:
                        pass

            if rightMouseClicked == True:
                self.Plansza[myszka[0]/CELLSIZE][myszka[1]/CELLSIZE].obiekt = None
                for i in self.Elementy:
                    if i.isClicked():
                        if i.nazwa == "sa":
                            smieciarkaNaPlanszy = False
                        self.Elementy.remove(i)

            for i in self.Elementy:
                i.rysuj()

            obiekt.Poz = (myszka[0]/CELLSIZE,myszka[1]/CELLSIZE)
            obiekt.rysuj()
   
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

    def zapytanie(self,Tresc):
        textinput = pygame_textinput.TextInput()
        textinput.set_text_color(RED)
        textinput.set_cursor_color(RED)
        textinput.input_string = "tester3"
        textinput.cursor_position = len(textinput.input_string)
        x = CELLCOUNTX/2
        y = WINDOWHEIGHT/2-2*CELLSIZE
        rect = pygame.Rect(x, y, CELLSIZE*61, CELLSIZE*5)
        Text = self.BASICFONT.render(Tresc, 1, BLACK)
        while True:
            events = pygame.event.get()
        
            for event in events:
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return ""
        
            self.DISPLAYSURF.fill(BGCOLOR)
            pygame.draw.rect(self.DISPLAYSURF, WHITE, rect)
            self.DISPLAYSURF.blit(Text, (x, y))
            self.DISPLAYSURF.blit(textinput.get_surface(), (x, y+25))

            if textinput.update(events):
                return textinput.get_text()
        
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

    def rysujSiatke(self):
        for x in range(0, WINDOWWIDTH, CELLSIZE):
            pygame.draw.line(self.DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE):
            pygame.draw.line(self.DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

class Odpowiadacz:

    def __init__(self,gra):
        self.gra = gra
        self.Poz = (0,35)
        self.TextOdpowiedz = self.gra.BASICFONT.render("", 1, WHITE)
    
    def ustawDopowiedz(self, Odpowiedz):
        self.TextOdpowiedz = self.gra.BASICFONT.render(Odpowiedz, 1, WHITE)
        print Odpowiedz

    def rysuj(self):
        self.gra.DISPLAYSURF.blit(self.TextOdpowiedz, (self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE))

class Punkt:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.gCost = float()
        self.hCost = float()
        self.walkable = True
        self.parent = None
        self.obiekt = None

    def fCost(self):
        return self.gCost + self.hCost

    def __lt__(self, other):
        if self.fCost() == other.fCost():
            return self.hCost < other.hCost
        return self.fCost() < other.fCost()

class Aktor:
    def tick(self, ticks): pass
    def rysuj(self): pass
    def isClicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def __init__(self,x,y,nazwa,gra):
        self.Poz = (x,y)
        self.rect = pygame.Rect(self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE, CELLSIZE, CELLSIZE)
        self.nazwa = nazwa
        self.gra = gra

class Smieciarka(Aktor):
    
    def __init__(self,x,y,gra):
        Aktor.__init__(self,x,y,"sa",gra)
        self.zaladunek = 0
        self.TextZaladunek = self.gra.BASICFONT.render(str(self.zaladunek)+ "%", 1, RED)
        self.LastTick = 0
        self.cooldown = 100
        self.Trasa = []
        self.odpowiadacz = Odpowiadacz(gra)
        self.KolejkaZadan = Queue.Queue()
        self.Lock = False
        self.CelDojazdu = (-1,-1)

    def get(self):
        return self
        
    def zaladuj(self, ilosc):
        self.zaladunek += ilosc

    def rozladuj(self):
        for neighbour in self.getNeighbours(self.gra.Plansza[self.Poz[0]][self.Poz[1]]):
            if neighbour.obiekt != None and neighbour.obiekt.nazwa == "wy":
                self.zaladunek = 0

    def rysuj(self):
        self.rect = pygame.Rect(self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE, CELLSIZE, CELLSIZE)
        pygame.draw.rect(self.gra.DISPLAYSURF, WHITE, self.rect)
        self.gra.DISPLAYSURF.blit(self.TextZaladunek, (self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE))
        self.odpowiadacz.rysuj()

    def ustaw(self, x,y):
        self.gra.Plansza[self.Poz[0]][self.Poz[1]].obiekt = None
        self.gra.Plansza[self.Poz[0]][self.Poz[1]].walkable = True
        self.Poz = (x,y)
        self.gra.Plansza[self.Poz[0]][self.Poz[1]].walkable = False
        self.gra.Plansza[self.Poz[0]][self.Poz[1]].obiekt = self

    def tick(self, ticks):
        self.TextZaladunek = self.gra.BASICFONT.render(str(self.zaladunek)+ "%", 1, RED)
        if self.CelDojazdu == self.Poz and self.Lock:
            self.Lock = False
        if ticks - self.LastTick >= self.cooldown:
            self.LastTick = ticks
            if self.Trasa:
                Cel = self.Trasa.pop()
                self.ustaw(Cel.x,Cel.y)
            elif not self.KolejkaZadan.empty() and not self.Lock:
                zadanie = self.KolejkaZadan.get()
                funkcja = zadanie[0]
                argumenty = zadanie[1:]
                funkcja(*argumenty)

    def getNeighbours(self, punkt):
        neighbours = list()
        sprawdz = [(-1,0),(0,1),(0,-1),(1,0)]
        for x,y in sprawdz:
            sprawdzx = punkt.x + x
            sprawdzy = punkt.y + y
            if sprawdzx >=0 and sprawdzx < CELLCOUNTX and sprawdzy >=0 and sprawdzy < CELLCOUNTY:
                neighbours.append(self.gra.Plansza[sprawdzx][sprawdzy])
        return neighbours

    def getDistance(self, Punkt1, Punkt2):
        dstX = abs(Punkt1.x - Punkt2.x)
        dstY = abs(Punkt1.y - Punkt2.y)
        if dstX > dstY:
            return 1*dstX + 1*(dstX-dstY)
        return 1*dstX + 1*(dstY-dstX)

    def znajdzTrase(self, Cel):
        if Cel.walkable == False:
            self.odpowiadacz.ustawDopowiedz(U"Trasa niemożliwa")
            self.Lock = False
            return
        self.CelDojazdu = (Cel.x,Cel.y)
        self.Lock = True
        #self.odpowiadacz.ustawDopowiedz("Szukam trasy...")
        czasstart = time.time()
        start = self.gra.Plansza[self.Poz[0]][self.Poz[1]]
        closedSet = []
        openSet = []
        heapq.heapify(openSet)
        heapq.heappush(openSet,start)

        while openSet:
            current = heapq.heappop(openSet)      
            if current == Cel:
                czasend = time.time()
                #self.odpowiadacz.ustawDopowiedz("Znaleziono trase w czasie: " + str(czasend - czasstart) + " sekundy.")
                return self.zrekonstruujTrase(start, Cel)

            closedSet.append(current)

            for neighbour in self.getNeighbours(current):
                if not neighbour.walkable or neighbour in closedSet:
                    continue
                tentative_gScore = current.gCost + self.getDistance(current, neighbour)
                if tentative_gScore < neighbour.gCost or neighbour not in openSet:
                    neighbour.gCost = tentative_gScore
                    neighbour.hCost = self.getDistance(neighbour, Cel)
                    neighbour.parent = current

                    if neighbour not in openSet:
                        heapq.heappush(openSet,neighbour)
        self.odpowiadacz.ustawDopowiedz(U"Trasa niemożliwa")
        self.Lock = False
        return

    def zrekonstruujTrase(self, start, koniec):
        Trasa = list()
        current = koniec
        while current != start:
            Trasa.append(current)
            current = current.parent
        self.Trasa = Trasa

    def ustawKolejke(self,kolejka):
        self.KolejkaZadan = kolejka

    def oproznijKosz(self):
        for neighbour in self.getNeighbours(self.gra.Plansza[self.Poz[0]][self.Poz[1]]):
            if neighbour.obiekt != None and (neighbour.obiekt.nazwa == "sk" or neighbour.obiekt.nazwa == "sm" or neighbour.obiekt.nazwa == "sl" or neighbour.obiekt.nazwa == "sp"):
                if neighbour.obiekt.podajIloscSmieci()/10 + self.zaladunek <= 100:
                    self.zaladuj(neighbour.obiekt.oproznij()/10)
                else:
                    tymczasowaKolejka = Queue.Queue()
                    cel = self.gra.Wysypisko.PunktDostarczenia
                    cel2 = self.Poz
                    tymczasowaKolejka.put((self.odpowiadacz.ustawDopowiedz,(U'Brak miejsca. Wysypuję na wysypisku')))
                    tymczasowaKolejka.put( (thread.start_new_thread, self.znajdzTrase, (self.gra.Plansza[cel[0]][cel[1]], )) )
                    tymczasowaKolejka.put((self.rozladuj,))
                    tymczasowaKolejka.put((self.odpowiadacz.ustawDopowiedz,(U'Rozładowywanie śmieciarki')))
                    tymczasowaKolejka.put((thread.start_new_thread, self.znajdzTrase, (self.gra.Plansza[cel2[0]][cel2[1]],)))
                    tymczasowaKolejka.put((self.oproznijKosz,))
                    tymczasowaKolejka.put((self.odpowiadacz.ustawDopowiedz, (U'Odebranie śmieci') ))
                    tymczasowaKolejka.put((self.ustawKolejke, (self.KolejkaZadan)))
                    self.KolejkaZadan = tymczasowaKolejka
        
class Smietnik(Aktor):
    
    def __init__(self,x,y,gra,ID,kolor,nazwa):
        Aktor.__init__(self,x,y,nazwa,gra)
        self.iloscSmieci = 0
        self.IDFONT = pygame.font.SysFont("monospace", 10)
        self.TextIloscSmieci = self.gra.BASICFONT.render(str(self.iloscSmieci)+ "%", 1 , RED)
        self.LastTick = 0
        self.cooldown = random.randint(2000, 3000)
        self.kolor = kolor
        self.ID = ID
        if ID < 100:
            self.TextID = self.gra.BASICFONT.render(str(ID), 1, RED)
        else:
            self.TextID = self.IDFONT.render(str(ID), 1, RED)
        self.PunktOdbioru = self.znajdzWolnePole()
        if CELLCOUNTX/2 > x:
            self.Zachod = True
        else:
            self.Zachod = False
        if CELLCOUNTY/2 > y:
            self.Polnoc = True
        else:
            self.Polnoc = False
      
    
    def dodaj(self, ilosc):
        if (self.iloscSmieci + ilosc <= 100):
            self.iloscSmieci = self.iloscSmieci + ilosc
            return True
        return False

    def oproznij(self):
        a = self.iloscSmieci
        self.iloscSmieci = 0
        return a

    def podajIloscSmieci(self):
        return self.iloscSmieci

    def znajdzWolnePole(self):
        sprawdz = [(-1,0),(0,1),(0,-1),(1,0)]
        for x,y in sprawdz:
            sprawdzx = self.Poz[0] + x
            sprawdzy = self.Poz[1] + y
            if sprawdzx >=0 and sprawdzx < CELLCOUNTX and sprawdzy >=0 and sprawdzy < CELLCOUNTY and self.gra.Plansza[sprawdzx][sprawdzy].obiekt == None:
                return (sprawdzx,sprawdzy)

    def rysuj(self):
        self.rect = pygame.Rect(self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE, CELLSIZE, CELLSIZE)
        pygame.draw.rect(self.gra.DISPLAYSURF, self.kolor, self.rect)
        self.gra.DISPLAYSURF.blit(self.TextIloscSmieci, (self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE))
        self.gra.DISPLAYSURF.blit(self.TextID, (self.PunktOdbioru[0] * CELLSIZE, self.PunktOdbioru[1] * CELLSIZE))

    def tick(self, ticks):
        self.TextIloscSmieci = self.gra.BASICFONT.render(str(self.iloscSmieci) +"%", 1, RED)
        if ticks - self.LastTick >= self.cooldown:
            self.LastTick = ticks
            self.dodaj(1)

class SmietnikMakulatura(Smietnik):

    def __init__(self,x,y,gra,ID):
        Smietnik.__init__(self,x,y,gra,ID,BLUE,"sm")

class SmietnikPlastik(Smietnik):

    def __init__(self,x,y,gra,ID):
        Smietnik.__init__(self,x,y,gra,ID,YELLOW,"sp")

class SmietnikSzklo(Smietnik):

    def __init__(self,x,y,gra,ID):
        Smietnik.__init__(self,x,y,gra,ID,GREEN,"sk")

class SmietnikAluminium(Smietnik):

    def __init__(self,x,y,gra,ID):
        Smietnik.__init__(self,x,y,gra,ID,ORANGE,"sl")

class Sciana(Aktor):

    def __init__(self,x,y,gra):
        Aktor.__init__(self,x,y,"sc",gra)

    def rysuj(self):
        self.rect = pygame.Rect(self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE, CELLSIZE, CELLSIZE)
        pygame.draw.rect(self.gra.DISPLAYSURF, DARKGRAY, self.rect)

class Wysypisko(Aktor):

    def __init__(self,x,y,gra):
        Aktor.__init__(self,x,y,"wy",gra)
        self.PunktDostarczenia = self.znajdzWolnePole()

    def znajdzWolnePole(self):
        sprawdz = [(-1,0),(0,1),(0,-1),(1,0)]
        for x,y in sprawdz:
            sprawdzx = self.Poz[0] + x
            sprawdzy = self.Poz[1] + y
            if sprawdzx >=0 and sprawdzx < CELLCOUNTX and sprawdzy >=0 and sprawdzy < CELLCOUNTY and self.gra.Plansza[sprawdzx][sprawdzy].obiekt == None:
                return (sprawdzx,sprawdzy)

    def rysuj(self):
        self.rect = pygame.Rect(self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE, CELLSIZE, CELLSIZE)
        pygame.draw.rect(self.gra.DISPLAYSURF, BROWN, self.rect)

class Przycisk(Aktor):
    
    def __init__(self,x,y,Tresc, funkcja, RozmiarX, RozmiarY,gra):
        Aktor.__init__(self,x,y,"prz",gra)
        self.RozmiarX = RozmiarX
        self.RozmiarY = RozmiarY
        self.rect = pygame.Rect(self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE, CELLSIZE * RozmiarX, CELLSIZE * RozmiarY)
        self.Text = self.gra.BASICFONT.render(Tresc, 1, BLACK)
        self.funkcja = funkcja

    def rysuj(self):
        pygame.draw.rect(self.gra.DISPLAYSURF, WHITE, self.rect)
        self.gra.DISPLAYSURF.blit(self.Text, (self.Poz[0] * CELLSIZE, self.Poz[1] * CELLSIZE))
        
if __name__ == '__main__':
    main()
