from time import sleep
import my_functions
import requests
from bs4 import BeautifulSoup
import pandas

dane_testowe = [
    {
        "Nazwa": "Lwowska",
        "Link": "https://www.otodom.pl/pl/oferta/2-pok-kamienica-pl-politechniki-lwowska-metro-ID43OxW.html",
    },
    #  {'Nazwa': 'TEST1', 'Link': 'https://www.otodom.pl/pl/oferta/spokoj-i-bezpieczenstwo-dla-dwoch-rodzin-ID4gNwj'},
    #  {'Nazwa': 'TEST2', 'Link': 'https://www.otodom.pl/pl/oferta/nowe-mieszk-4pok-z-balkonem-i-tarasem-przy-lesie-ID49nnI'}
    #  {"Nazwa": "TEST2", "Link": "https://www.otodom.pl/pl/oferta/mieszkanie-45-30-m-warszawa-ID4huua"}
]

PLIK_DANE = "oto-dom.xlsx"
PLIK_LOG = "oto-dom.log"


def readDataFromSite(url):
    response = requests.get(
        url,
        headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.87 Safari/537.36"
        },
    )
    webpage = response.text
    soup = BeautifulSoup(webpage, "lxml")

    # Zapis kodu strony do pliku
    # with open("html.html", "w", encoding="utf-8") as f:
    #     f.write(soup.prettify())

    # Tytuł
    elems = soup.select_one("header.css-1s2plby.eu6swcv26")
    if elems is None:
        elems = soup.select_one("header.css-1sgd721.eu6swcv25")
    if elems is None:
        elems = soup.select_one("header")
    if elems is not None:
        tytul = elems.select_one("h1").get_text().strip()
        cena = elems.select_one("strong.css-8qi9av.eu6swcv19").get_text().strip()
        lok = elems.select_one("a.e1nbpvi60.css-1kforri.e1enecw71").get_text().strip()
        cena_m2 = elems.select_one("div.css-1p44dor.eu6swcv16").get_text().strip()

        # Szczegóły ogłoszenia
        # Spacja oznacza że znacznik jest gdzieś niżej
        elems = soup.select("div.css-wj4wb2.emxfhao1 div.css-1qzszy5.estckra8")
        pow = elems[1].get_text().strip()
        wlasnosc = elems[3].get_text().strip()
        pokoje = elems[5].get_text().strip()
        wykonczenie = elems[7].get_text().strip()
        pietro = elems[9].get_text().strip()
        balkon = elems[11].get_text().strip()
        garaz = elems[15].get_text().strip()

        # Opis
        # znak > oznacza że znacznik jest bezpośrednio niżej
        elems = soup.select_one("section.css-3hljba.e1r1048u3 > div")
        opis = elems.get_text().strip()

        # Informacje dodatkowe
        # Spacja oznacza że znacznik jest gdzieś niżej
        elems = soup.select(
            "div.css-1l1r91c.emxfhao1 div.css-f45csg.estckra9 div.estckra8"
        )
        rynek = elems[1].get_text().strip()
        ogloszenie = elems[3].get_text().strip()
        winda = elems[13].get_text().strip()

        # print(tytul,cena, lok, cena_m2)
        # print(pow, wlasnosc, pokoje, wykonczenie, pietro, balkon, garaz)
        # print(rynek, ogloszenie, winda)
        # print(opis)

        dane_strony = [
            {
                "Data": my_functions.getCurrentTime(),
                "Tytuł": tytul,
                "Cena": cena,
                "Cena/m²": cena_m2,
                "Powierzchnia": pow,
                "Lokalizacja": lok,
                "Typ ogłoszenia": ogloszenie,
                "Własność": wlasnosc,
                "Liczba pokoi": pokoje,
                "Wykończenie": wykonczenie,
                "Piętro": pietro,
                "Balkon": balkon,
                "Garaż": garaz,
                "Winda": winda,
                "Rynek": rynek,
                "Opis": opis,
            }
        ]

        df = pandas.DataFrame(dane_strony)

        # print(df)

        return df


def logowanie(tekst, plik):
    print(tekst, file=plik)
    print(tekst)


def main():
    TEST = False
    plik_logow = open(PLIK_LOG, "w")

    try:
        if TEST:
            dane = dane_testowe
        else:
            dane = my_functions.readLinksFromExcel(PLIK_DANE)
    except FileNotFoundError:
        logowanie("Brak pliku danych: " + PLIK_DANE, plik_logow)
        dane = []

    if len(dane) > 0:
        try:
            for dom in dane:
                xl = pandas.ExcelFile(PLIK_DANE)
                arkusze = xl.sheet_names

                nazwa_oferty = dom["Nazwa"]
                logowanie(nazwa_oferty, plik_logow)

                strona_df = readDataFromSite(dom["Link"])
                if strona_df is None:
                    logowanie("--- Oferta nie istnieje na podanej stronie", plik_logow)
                else:
                    with pandas.ExcelWriter(
                        PLIK_DANE, mode="a", if_sheet_exists="overlay"
                    ) as writer:
                        if nazwa_oferty in arkusze:
                            plik_df = xl.parse(nazwa_oferty)
                            polaczony_df = pandas.concat([strona_df, plik_df])
                            polaczony_df.to_excel(
                                writer, sheet_name=nazwa_oferty, index=False
                            )
                        else:
                            strona_df.to_excel(
                                writer, sheet_name=nazwa_oferty, index=False
                            )
        except PermissionError:
            logowanie("Błąd dostępu do pliku z danymi:" + PLIK_DANE, plik_logow)
        except Exception as e:  # work on python 3.x
            logowanie("Inny błąd: " + str(e), plik_logow)
    else:
        logowanie("Brak ofert.", plik_logow)

    logowanie("--KONIEC--", plik_logow)
    plik_logow.close()


if __name__ == "__main__":
    main()
