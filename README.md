# DungeonCrawler
A game for 2020's Individual Programming Project
## PL:
## 1 Dane techniczne 
### Typ programu: 
Gra 2D z gatunku "Dungeon Crawler"
### Język programowania: 
Python 3.8
### Biblioteki: 
Silnik gry - Cocos2D 0.6.8

Pyglet 1.5.0 - Cocos2D jest na nim zbudowany
## 2 Cechy gry 
- Gra dla jednego gracza 
- Widok izometryczny/’z góry’ 
- Sytem progresji 
- Przeciwnicy zależni od poziomu progresji gracza 
- Generator losowych poziomów
- Zapis gry po każdym ukończonym poziomie
- Opcje gry: zmiana rozdzielczości, trybu wyświetlania (pełny ekran/okno)
## 3 Krótki opis rozgrywki: 
Gracz steruje postacią poruszającą się po lochach/jaskiniach, podczas ich eksploracji walcząc z przeciwnikami, znajdując nowe, pomocne w rozgrywce przedmioty (np. nowe uzbrojenie), i co jakiś czas mając możliwość podniesienia jednej ze statystyk swojej postaci (takiej jak siła, zręczność itd.). Przeciwnicy wraz z postępami gracza również stają się odpowiednio potężniejsi, by zachować element wyzwania. Kolejne poziomy konstruowane są przez generator.

## ENG:
## 1 Technical data
### Program type:
A 2D Game, genre: "Dungeon Crawler"
### Programming language:
Python 3.8
### Libraries:
Game engine - Cocos2D 0.6.8

Pyglet 1.5.0 - necessary for Cocos2D to run
## 2 Game features:
- single-player game 
- 3rd person perspective 
- Progression system
- Enemies dependant on the player's progression
- Level generator
- Option to save a game state after every completed level
- Game options include changing the game's resolution and display mode (fullscreen/window)
## 3 Gameplay:
The player controls a character traversing through dungeons/cave systems, exploring them and fighting with various enemies along the way. During the game the player can pick up various, helpful items (eg. new armor), and has the ability to rise the character's statiscics (like strength, agility and such). The more powerful the player becomes, the harder enemies he encounters, keeping the game challenging. Levels are constructed using the in-game level generator.


----------------------------------------------------------------------------------------------------------------------------
### Raport z postępu prac (23.04.2020):
Zaimplementowane:
## Menu główne:
- Działające przejście z menu do właściwej gry
- Opcje:
> Zmiana trybu wyświetlania: okno/pełny ekran

> Włączenie/wyłączenie licznika FPS
- Wyjście z aplikacji
## Rozgrywka:
- Rysowanie - gracz, poziom, wstępne handlery na przeciwników
- Generator losowych poziomów - prosta generacja losowych przeszkód na poziomie, do rozwinięcia
- Sterowanie graczem - podstawowe ruchy + zmienne przyspieszenie postaci
- Detekcja kolizji - zaimplementowane (jeszcze do zdebugowania), napisane handlery na przyszłe postacie przeciwników
- Stworzenie i zaimplementowanie testowych sprite-ów gracza i sceny

Koncepcja gry, oraz używane biblioteki (oraz ich wersja) nie uległy zmianie.

----------------------------------------------------------------------------------------------------------------------------
### Raport z postępu prac (28.05.2020):
Zaimplementowane:
## Rozgrywka:
- Poprawa generatora poziomów - przejścia pomiędzy poziomami
- Stworzenie wstępnych sprite-ów gracza, otoczenia, przeciwników
- Zaprojektowanie menu ekwipunku gracza
- Wrogowie oraz ich statystyki
- Model walki/interakcji pomiędzy przeciwnikiem a graczem

Koncepcja gry, oraz używane biblioteki (oraz ich wersja) nie uległy zmianie.\
Uwaga: Kod na repozytorium może różnić się od obecnej wersji gry, obecnie testuję różne warianty rozgrywki. Aktualizacja na repozytorium pojawi się niebawem.


----------------------------------------------------------------------------------------------------------------------------
### Końcowy stan projektu - Battlefield Crawler:


# Koncepcja:
Planowane | Finalna wersja
------------ | -------------
Gracz steruje postacią poruszającą się po lochach/jaskiniach, walcząc z przeciwnikami, znajdując nowe, pomocne w rozgrywce przedmioty (np. nowe uzbrojenie), i co jakiś czas mając możliwość podniesienia jednej ze statystyk swojej postaci (takiej jak siła, zręczność itd.). Przeciwnicy wraz z postępami gracza również stają się odpowiednio potężniejsi, by zachować element wyzwania| Gracz porusza się po zbombardowanej plaży na którą został zrzucony, omija miny, kontakt z którymi zabiera zdrowie bohatera. Co poziom lizebność i ilość zabieranego przez przeszkody zdrowia wzrasta. Co 5 poziomów na mapie pojawia się apteczka, którą można uleczyć rany.

# Informacje techniczne
Planowane | Finalna wersja
------------ | -------------
Język: Python 3.8 | :heavy_check_mark:
Używane biblioteki: Cocos2D 0.6.8, Pyglet 1.5.0 | :heavy_check_mark:
Widok izometryczny/ "z góry" | :heavy_check_mark:
Ekwipunek | Zaprojektowano, nie zaimplementowano :x:
System progresji: Statystyki gracza | Zdrowie :heavy_check_mark:, Kondycja :heavy_check_mark:, Poziom :heavy_check_mark:
System progresji: Przeciwnicy zależni od poziomu progresji gracza  | Co poziom przeciwnicy zabierają przy kontakcie coraz więcej zdrowia, są coraz liczniejsi :heavy_check_mark:
Generator losowych poziomów | Losowo rozstawiani przeciwnicy i przeszkody :heavy_check_mark:, "Inteligentne" generowanie poziomu: przeszkody ani przeciwnicy nie nachodzą na siebie :heavy_check_mark:
Zapis gry po każdym ukończonym poziomie |
Opcje gry: zmiana rozdzielczości, trybu wyświetlania (pełny ekran/okno) | Zaimplementowano :heavy_check_mark:, dodatkowo licznik klatek na sekundę :heavy_check_mark:

