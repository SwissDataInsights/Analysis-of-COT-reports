import os
import pandas as pd
import mplfinance as mpf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Definiowanie słownika firm notowanych na giełdzie w Szwajcarii
companies = {
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

# Funkcja do obliczania wskaźnika RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Ustal współczynnik dla pasm Bollingera
band_width_factor = 1.5

# Tworzenie pliku PDF, w którym zapiszemy wszystkie wykresy
with PdfPages('Swiss_Stock_Charts.pdf') as pdf:
    # Iteracja przez każdą firmę w słowniku
    for i, (symbol, company_name) in enumerate(companies.items()):
        # Załaduj dane dzienne (D1)
        file_path_d1 = f"{company_name}_data_D1.xlsx"
        if not os.path.exists(file_path_d1):
            print(f"Brak danych dla {company_name}. Plik nie istnieje.")
            continue
        data_d1 = pd.read_excel(file_path_d1, index_col=0, parse_dates=True)

        # Ograniczenie danych do ostatnich 60 obserwacji
        data_d1 = data_d1.tail(60)

        # Załaduj dane tygodniowe (W1)
        file_path_1w = f"{company_name}_data_W1.xlsx"
        if not os.path.exists(file_path_1w):
            print(f"Brak danych dla {company_name}. Plik nie istnieje.")
            continue
        data_1w = pd.read_excel(file_path_1w, index_col=0, parse_dates=True)

        # Oblicz medianę z 6 okresów dla danych dziennych (D1)
        data_d1['6_Period_Median_D1'] = data_d1['Close'].rolling(window=6).median()

        # Oblicz medianę z 6 okresów dla danych tygodniowych (W1)
        data_1w['6_Period_Median_W1'] = data_1w['Close'].rolling(window=6).median()

        # Oblicz odchylenie standardowe dla pasm Bollingera
        data_1w['Rolling_Std'] = data_1w['Close'].rolling(window=6).std()

        # Wyznacz górną i dolną bandę w oparciu o pasma Bollingera z modyfikowanym współczynnikiem
        data_1w['Upper_Bollinger'] = data_1w['6_Period_Median_W1'] + band_width_factor * data_1w['Rolling_Std']
        data_1w['Lower_Bollinger'] = data_1w['6_Period_Median_W1'] - band_width_factor * data_1w['Rolling_Std']

        # Wyrównaj dane tygodniowe do tego samego indeksu co dane dzienne
        data_1w_reindexed = data_1w.reindex(data_d1.index, method='ffill')

        # Oblicz RSI
        data_d1['RSI'] = calculate_rsi(data_d1)

        # Przygotowanie danych do rysowania świec (dla danych dziennych)
        data_d1.index = pd.to_datetime(data_d1.index)

        # Pobranie ostatniej wartości mediany i band
        last_median_d1 = data_d1['6_Period_Median_D1'].iloc[-1]
        last_median_w1 = data_1w_reindexed['6_Period_Median_W1'].iloc[-1]

        # Tworzenie dodatkowych danych do rysowania (mediana, pasma, RSI)
        ap = [
            mpf.make_addplot(data_d1['6_Period_Median_D1'], color='orange', label=f'6-Period Median D1: {last_median_d1:.2f}'),
            mpf.make_addplot(data_1w_reindexed['6_Period_Median_W1'], color='purple', label=f'6-Period Median W1: {last_median_w1:.2f}'),
            mpf.make_addplot(data_1w_reindexed['Upper_Bollinger'], color='green', linestyle='dashed', label=f'Upper Bollinger W1'),
            mpf.make_addplot(data_1w_reindexed['Lower_Bollinger'], color='red', linestyle='dashed', label=f'Lower Bollinger W1'),
            mpf.make_addplot(data_d1['RSI'], color='blue', panel=1, ylabel='RSI')  # Dodanie wskaźnika RSI
        ]

        # Tworzenie wykresu świecowego z medianą D1, W1, pasmami Bollingera, wolumenem i RSI
        fig, ax = mpf.plot(data_d1, type='candle', style='charles', addplot=ap, volume=True,
                 title=company_name,  # Tylko nazwa spółki w tytule
                 ylabel='Price', returnfig=True)

        # Zmniejszenie czcionki tytułu, aby dopasować do PDF
        ax[0].set_title(company_name, fontsize=10)

        # Zapisanie wykresu do pliku PDF
        pdf.savefig(fig)  # Zapisanie figury do PDF
        plt.close(fig)  # Zamknięcie figury, aby nie zaśmiecać pamięci

print("Wszystkie wykresy zostały zapisane do pliku PDF.")
