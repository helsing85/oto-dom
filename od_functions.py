import datetime


def readLinksFromCSV(filepath):
    import pandas

    dane = pandas.read_csv(filepath, sep=";", encoding="windows-1250")
    dane_list = [
        {"Nazwa": row["Nazwa"], "Link": row["Link"]} for (index, row) in dane.iterrows()
    ]

    # print(dane_list)
    return dane_list


def readLinksFromExcel(filepath):
    import pandas

    dane = pandas.read_excel(filepath, sheet_name=0)
    dane_list = [
        {"Nazwa": row["Nazwa"], "Link": row["Link"]} for (index, row) in dane.iterrows()
    ]

    # print(dane_list)
    return dane_list


def getCurrentTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
