import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Funkcja do obliczenia RSI z zaokrągleniem do pełnych jednostek
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.round(0)  # Zaokrąglenie RSI do pełnych jednostek

# Funkcja do obliczenia 6-okresowej mediany z zaokrągleniem do dwóch miejsc po przecinku
def calculate_rolling_median(data, window=6):
    return data['Close'].rolling(window=window).median().round(2)

# Funkcja do obliczenia pasm Bollingera z zaokrągleniem do dwóch miejsc po przecinku
def calculate_bollinger_bands(data, window=6, band_width_factor=1.5):
    rolling_std = data['Close'].rolling(window=window).std()
    rolling_median = calculate_rolling_median(data, window=window)
    upper_band = (rolling_median + band_width_factor * rolling_std).round(2)
    lower_band = (rolling_median - band_width_factor * rolling_std).round(2)
    return upper_band, lower_band

# Definiowanie słownika firm notowanych na giełdzie w Szwajcarii
companies = {
    'EURUSD=X': 'EURUSD=X',
    'SREN.SW': 'SwissReAG',
    'ABBN.SW': 'ABB_Ltd',
    'ALC.SW': 'Alcon',
    'GEBN.SW': 'Geberit',
    'GIVN.SW': 'Givaudan',
    'HOLN.SW': 'Holcim',
    'KNIN.SW': 'KuehneNagel',
    'LOGN.SW': 'Logitech',
    'LONN.SW': 'Lonza',
    'NESN.SW': 'Nestle',
    'NOVN.SW': 'Novartis',
    'PGHN.SW': 'PartnersGroup',
    'CFR.SW': 'Richemont',
    'ROG.SW': 'Roche',
    'SIKA.SW': 'Sika',
    'SOON.SW': 'Sonova',
    'SLHN.SW': 'SwissLife',
    'SCMN.SW': 'Swisscom',
    'UBSG.SW': 'UBS',
    'ZURN.SW': 'ZurichInsurance'
}

# Ustal zakres dat - ostatnie 4 lata
end_date = datetime.today()
start_date = end_date - timedelta(days=1440)  # 4 lata

# Iteracja przez każdą firmę w słowniku
for symbol, company_name in companies.items():
    output_file_d1 = f"{company_name}_data_D1.xlsx"
    output_file_1w = f"{company_name}_data_W1.xlsx"

    # Sprawdź, czy plik istnieje, i usuń go (dla danych D1)
    if os.path.exists(output_file_d1):
        os.remove(output_file_d1)
        print(f"Usunięto stary plik {output_file_d1}")

    # Pobierz nowe dane dzienne (D1)
    data_d1 = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval="1d")

    # Sprawdź, czy dane dzienne zostały pobrane
    if not data_d1.empty:
        # Upewnij się, że indeks jest w formacie DatetimeIndex
        data_d1.index = pd.to_datetime(data_d1.index)

        # Obliczanie RSI i Mediany 6-okresowej
        data_d1['RSI'] = calculate_rsi(data_d1)
        data_d1['Median_6'] = calculate_rolling_median(data_d1)

        # Obliczanie pasm Bollingera
        data_d1['BG'], data_d1['BD'] = calculate_bollinger_bands(data_d1)

        # Usunięcie najstarszych 13 wierszy
        data_d1 = data_d1.iloc[13:]

        # Zapisz dane dzienne do pliku Excel
        data_d1.to_excel(output_file_d1)
        print(f"Dane dzienne zapisane do pliku {output_file_d1}")
    else:
        print(f"Nie udało się pobrać danych dziennych dla {symbol}.")

    # Sprawdź, czy plik istnieje, i usuń go (dla danych 1W)
    if os.path.exists(output_file_1w):
        os.remove(output_file_1w)
        print(f"Usunięto stary plik {output_file_1w}")

    # Pobierz nowe dane tygodniowe (1W)
    data_1w = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval="1wk")

    # Sprawdź, czy dane tygodniowe zostały pobrane
    if not data_1w.empty:
        # Upewnij się, że indeks jest w formacie DatetimeIndex
        data_1w.index = pd.to_datetime(data_1w.index)

        # Obliczanie RSI i Mediany 6-okresowej
        data_1w['RSI'] = calculate_rsi(data_1w)
        data_1w['Median_6'] = calculate_rolling_median(data_1w)

        # Obliczanie pasm Bollingera
        data_1w['BG'], data_1w['BD'] = calculate_bollinger_bands(data_1w)

        # Usunięcie najstarszych 13 wierszy
        data_1w = data_1w.iloc[13:]

        # Zapisz dane tygodniowe do pliku Excel
        data_1w.to_excel(output_file_1w)
        print(f"Dane tygodniowe zapisane do pliku {output_file_1w}")
    else:
        print(f"Nie udało się pobrać danych tygodniowych dla {symbol}.")
