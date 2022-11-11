from asyncio.windows_events import NULL
import pandas
import od_functions
from od_webdriver import *

PLIK_DANE = "oto-dom.xlsx"
PLIK_LOG = "oto-dom.log"


def elementsByXpath(value):
    return DRV.find_elements(by=By.XPATH, value=value)


def tryFindElementByXpath(value):
    try:
        txt = DRV.find_element(by=By.XPATH, value=value).text
    except NoSuchElementException:
        txt = "brak danych"

    return txt


def readDataFromSiteSelenium(url):
    DRV.get(url)

    # Potwierdź cisteczka
    confirm_button = DRV.find_elements(by=By.ID, value="onetrust-accept-btn-handler")
    if len(confirm_button) > 0:
        confirm_button[0].click()

    # Przesuń stronę na dół
    # DRV.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # Tytuł
    elem = DRV.find_elements(by=By.TAG_NAME, value="header")
    if len(elem) > 0:
        try:
            tytul = elem[0].find_element(by=By.TAG_NAME, value="h1").text
            cena = elem[0].find_element(by=By.TAG_NAME, value="strong").text
            lok = elem[0].find_element(by=By.XPATH, value="./div[3]").text
            cena_m2 = elem[0].find_element(by=By.XPATH, value="./div[4]").text
        except NoSuchElementException as e:
            return

        # Szczegóły ogłoszenia
        elem = elementsByXpath("/html/body/div[1]/main/div[2]/div[2]/div[1]/div")
        if len(elem) == 0:
            elem = elementsByXpath("/html/body/div[1]/main/div[3]/div[2]/div[1]/div")

        pow = elem[0].find_element(by=By.XPATH, value="./div[1]/div[2]").text
        wlasnosc = elem[0].find_element(by=By.XPATH, value="./div[2]/div[2]").text
        pokoje = elem[0].find_element(by=By.XPATH, value="./div[3]/div[2]").text
        wykonczenie = elem[0].find_element(by=By.XPATH, value="./div[4]/div[2]").text
        pietro = elem[0].find_element(by=By.XPATH, value="./div[5]/div[2]").text
        balkon = elem[0].find_element(by=By.XPATH, value="./div[6]/div[2]").text
        garaz = elem[0].find_element(by=By.XPATH, value="./div[8]/div[2]").text

        # Opis
        elems = DRV.find_elements(by=By.TAG_NAME, value="section")
        opis = ""
        for elem in elems:
            if elem.text.startswith("Opis"):
                opis = elem.find_element(by=By.XPATH, value="./div").text
                break

        # Informacje dodatkowe
        rynek = tryFindElementByXpath("//div[@aria-label='Rynek']/div[2]")
        ogloszenie = tryFindElementByXpath(
            "//div[@aria-label='Typ ogłoszeniodawcy']/div[2]"
        )
        winda = tryFindElementByXpath("//div[@aria-label='Winda']/div[2]")

        # Daty
        dodano = DRV.find_element(
            by=By.XPATH, value="//div[contains(text(),'Data dodania')]"
        ).text.removeprefix("Data dodania: ")
        aktualizacja = DRV.find_element(
            by=By.XPATH, value="//div[contains(text(),'Data aktualizacji')]"
        ).text.removeprefix("Data aktualizacji: ")

        # print(tytul,cena, lok, cena_m2)
        # print(pow, wlasnosc, pokoje, wykonczenie, pietro, balkon, garaz)
        # print(rynek, ogloszenie, winda)
        # print(dodano, aktualizacja)
        # print(opis)

        dane_strony = [
            {
                "Data": od_functions.getCurrentTime(),
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
                "Dodano": dodano,
                "Aktualizacja": aktualizacja,
                "Opis": opis,
            }
        ]

        df = pandas.DataFrame(dane_strony)

        # print(df)

        return df


def logowanie(tekst, plik):
    print(tekst, file=plik)
    print(tekst)


def daneOgloszen(test):
    if test:
        dane_testowe = [
            {
                "Nazwa": "Chotomowska",
                "Link": "https://www.otodom.pl/pl/oferta/stara-ochota-kamienica-cisza-zielen-od-zaraz-ID4hU5f",
            },
            # {
            #     "Nazwa": "Barska",
            #     "Link": "https://www.otodom.pl/pl/oferta/stara-ochota-kamienica-54-m2-2-pok-ID4hFG3",
            # },
            # {
            #     "Nazwa": "Jankowska",
            #     "Link": "https://www.otodom.pl/pl/oferta/mieszkanie-3-pokojowe-ochota-ul-jankowska-ID4hj5U",
            # },
            # {
            #     "Nazwa": "TEST2",
            #     "Link": "https://www.otodom.pl/pl/oferta/nowe-mieszk-4pok-z-balkonem-i-tarasem-przy-lesie-ID49nnI",
            # },
            # {
            #     "Nazwa": "TEST2",
            #     "Link": "https://www.otodom.pl/pl/oferta/mieszkanie-45-30-m-warszawa-ID4huua",
            # },
        ]
        return dane_testowe
    else:
        return od_functions.readLinksFromExcel(PLIK_DANE)


def main():

    try:
        dane = daneOgloszen(test=False)
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

                try:
                    strona_df = readDataFromSiteSelenium(dom["Link"])
                except Exception as e:
                    logowanie("Błąd odczytu strony: " + str(e), plik_logow)
                    strona_df = None

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


if __name__ == "__main__":
    plik_logow = open(PLIK_LOG, "w")

    DRV = browserDriver(headless=True)
    if type(DRV) is str:
        logowanie(str, plik_logow)
    else:
        logowanie(type(DRV), plik_logow)
        main()
        DRV.quit()

    plik_logow.close()