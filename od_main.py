from asyncio.windows_events import NULL
import pandas
import od_functions
import od_test
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
    DRV.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # Tytuł
    elem = DRV.find_elements(by=By.TAG_NAME, value="header")
    if len(elem) > 0:
        try:
            tytul = tryFindElementByXpath("//h1[@data-cy='adPageAdTitle']")
            cena = tryFindElementByXpath("//strong[@aria-label='Cena']")
            lok = tryFindElementByXpath("//a[@aria-label='Adres']")
            cena_m2 = tryFindElementByXpath(
                "//div[@aria-label='Cena za metr kwadratowy']"
            )
        except NoSuchElementException as e:
            return

        # Szczegóły ogłoszenia
        pow = tryFindElementByXpath("//div[@aria-label='Powierzchnia']/div[2]")
        wlasnosc = tryFindElementByXpath("//div[@aria-label='Forma własności']/div[2]")
        pokoje = tryFindElementByXpath("//div[@aria-label='Liczba pokoi']/div[2]")
        wykonczenie = tryFindElementByXpath(
            "//div[@aria-label='Stan wykończenia']/div[2]"
        )
        pietro = tryFindElementByXpath("//div[@aria-label='Piętro']/div[2]")
        balkon = tryFindElementByXpath(
            "//div[@aria-label='Balkon / ogród / taras']/div[2]"
        )
        garaz = tryFindElementByXpath("//div[@aria-label='Miejsce parkingowe']/div[2]")

        # Opis
        # Pokaż więcej
        show_span = DRV.find_elements(
            by=By.XPATH, value="//span[contains(text(),'Pokaż więcej')]"
        )
        if len(show_span) > 0:
            show_button = show_span[0].find_element(by=By.XPATH, value="./..")
            show_button.click()

        opis = tryFindElementByXpath("//div[@data-testid='content-container']")

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

        # Odkryj numer telefonu
        phone_button = DRV.find_elements(
            by=By.XPATH,
            value="//a[contains(text(),'Zadzwoń')]",
        )
        if len(phone_button) > 0:
            phone_button = DRV.find_element(
                by=By.XPATH,
                value="//a[contains(text(),'Zadzwoń')]",
            )
            telefon = phone_button.get_attribute("href").removeprefix("tel:")
        else:
            phone_button = DRV.find_elements(
                by=By.XPATH,
                value="//button[@data-cy='phone-number.show-full-number-button']",
            )
            if len(phone_button) > 0:
                WebDriverWait(DRV, 20).until(
                    EC.element_to_be_clickable(phone_button[0])
                )
                try:
                    phone_button[0].click()
                    telefon = tryFindElementByXpath(
                        "//span[@data-cy='phone-number.full-phone-number']"
                    )
                except:
                    telefon = "brak danych"

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
                "Telefon": telefon,
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
        dane_testowe = od_test.dane_testowe
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
    DRV.maximize_window()
    if type(DRV) is str:
        logowanie(str, plik_logow)
    else:
        logowanie(type(DRV), plik_logow)
        main()
        DRV.quit()

    plik_logow.close()
