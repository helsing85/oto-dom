# oto-dom

oto-dom.xlsx - w pierwszej zakładce ("Oferty") należy podać Link oraz unikaną Nazwę dla oferty (bez znaków specjalnych).


Skrypt ("oto-dom.py") po uruchomieniu odczyta linki z pliku excel i ściągnie dane oferty z podanych linków. Dla każdej ofery stworzony zostanie oddzielny akrusz.
Nowe dane będą dodawane na początku arkusza. Każde uruchomienie skryptu doda nowy wiersz z danymi.

Przy działaniu tworzony jest plik "oto-dom.log" z podstawowymi logami z pracy aplikacji. Tam można sprawdzić że jakaś oferta wygasła i nie znaleiozno jej danych.

Do działania potrzebny jest webdriver przeglądarki. Obsługiwane są: Google Chrome, Microsoft Edge oraz Firefox.
W tej kolejności skrypt automatycznie wybierze przeglądarkę na podstawie znelezionych plików w folderze 'webdriver'.
