import backtrader as bt
import pandas as pd


# Definiowanie strategii
class CustomStrategy(bt.Strategy):
    params = (
        ('stop_loss_percentage', 0.30),  # 30% od mediany
        ('risk_to_reward_ratio', 2),  # Stosunek TP do SL
    )

    def __init__(self):
        self.median = self.data.median_6
        self.band_upper = self.data.BG  # Banda górna
        self.band_lower = self.data.BD  # Banda dolna
        self.prev_median = self.data.median_6(-1)  # Mediana z poprzedniego tygodnia
        self.sl_price = None
        self.tp_price = None

    def next(self):
        current_price = self.data.close[0]  # Pełna dokładność dla logiki
        median = self.median[0]  # Pełna dokładność dla logiki
        prev_median = self.prev_median[0]  # Pełna dokładność dla logiki
        band_upper = self.band_upper[0]  # Pełna dokładność dla logiki
        band_lower = self.band_lower[0]  # Pełna dokładność dla logiki

        # Warunki otwierania pozycji Long
        if self.position.size == 0 and median > prev_median and current_price > median:
            # Obliczanie SL i TP dla pozycji Long
            sl_value = median - (self.params.stop_loss_percentage * (median - band_lower))
            tp_value = band_upper

            # Sprawdzenie, czy stosunek TP/SL spełnia ustalony warunek
            if (tp_value - current_price) / (current_price - sl_value) >= self.params.risk_to_reward_ratio:
                self.sl_price = sl_value
                self.tp_price = tp_value
                print(
                    f"Otwieram pozycję Long przy cenie {round(current_price, 2)}, SL: {round(self.sl_price, 2)}, TP: {round(self.tp_price, 2)}")
                self.buy()  # Otwieranie pozycji Long

        # Warunki otwierania pozycji Short
        if self.position.size == 0 and median < prev_median and current_price < median:
            # Obliczanie SL i TP dla pozycji Short
            sl_value = median + (self.params.stop_loss_percentage * (band_upper - median))
            tp_value = band_lower

            # Sprawdzenie, czy stosunek TP/SL spełnia ustalony warunek
            if (current_price - tp_value) / (sl_value - current_price) >= self.params.risk_to_reward_ratio:
                self.sl_price = sl_value
                self.tp_price = tp_value
                print(
                    f"Otwieram pozycję Short przy cenie {round(current_price, 2)}, SL: {round(self.sl_price, 2)}, TP: {round(self.tp_price, 2)}")
                self.sell()  # Otwieranie pozycji Short

        # Warunki zamykania pozycji Long
        if self.position.size > 0:  # Pozycja Long
            # Zamknięcie, jeśli cena spada poniżej SL
            if current_price <= self.sl_price:
                print(f"Zamykam pozycję Long - SL osiągnięty, Cena: {round(current_price, 2)}")
                self.sell()

            # Zamknięcie, jeśli cena osiągnie TP
            if current_price >= self.tp_price:
                print(f"Zamykam pozycję Long - TP osiągnięty, Cena: {round(current_price, 2)}")
                self.sell()

            # Zamknięcie, jeśli mediana tygodniowa spada
            if median < prev_median:
                print(f"Zamykam pozycję Long - Mediana spada, Cena: {round(current_price, 2)}")
                self.sell()

        # Warunki zamykania pozycji Short
        if self.position.size < 0:  # Pozycja Short
            # Zamknięcie, jeśli cena wzrasta powyżej SL
            if current_price >= self.sl_price:
                print(f"Zamykam pozycję Short - SL osiągnięty, Cena: {round(current_price, 2)}")
                self.buy()

            # Zamknięcie, jeśli cena osiągnie TP
            if current_price <= self.tp_price:
                print(f"Zamykam pozycję Short - TP osiągnięty, Cena: {round(current_price, 2)}")
                self.buy()

            # Zamknięcie, jeśli mediana tygodniowa rośnie
            if median > prev_median:
                print(f"Zamykam pozycję Short - Mediana rośnie, Cena: {round(current_price, 2)}")
                self.buy()

        # Przesuwanie SL i TP dla pozycji Long
        if self.position.size > 0 and median > prev_median:
            self.sl_price = median - (self.params.stop_loss_percentage * (median - band_lower))
            self.tp_price = band_upper
            print(f"Przesuwam SL na {round(self.sl_price, 2)}, TP na {round(self.tp_price, 2)}")

        # Przesuwanie SL i TP dla pozycji Short
        if self.position.size < 0 and median < prev_median:
            self.sl_price = median + (self.params.stop_loss_percentage * (band_upper - median))
            self.tp_price = band_lower
            print(f"Przesuwam SL na {round(self.sl_price, 2)}, TP na {round(self.tp_price, 2)}")

    def notify_trade(self, trade):
        if trade.isclosed:
            print(f"Zysk/Strata na transakcji: {round(trade.pnl, 2)} zł")


# Funkcja do podsumowania wyników
def print_summary(analyzers):
    print('Statystyki:')
    print('-----------------------------------')
    print(f'Łączna liczba transakcji: {analyzers.ta.get_analysis()["total"]["total"]}')
    print(
        f'Procent zyskownych transakcji: {analyzers.ta.get_analysis()["won"]["total"] / analyzers.ta.get_analysis()["total"]["total"] * 100:.2f}%')
    print(f'Całkowity zysk/strata: {analyzers.ta.get_analysis()["pnl"]["net"]["total"]:.2f} zł')
    print(f'Maksymalne obsunięcie kapitału: {analyzers.drawdown.get_analysis()["max"]["drawdown"]:.2f}%')
    print(f'Wskaźnik Sharpe\'a: {analyzers.sharpe.get_analysis()["sharperatio"]:.2f}')


# Wczytanie danych z pliku Excel (SwissReAG_data_W1) i przypisanie mediany oraz bandy górnej i dolnej
w1_data = pd.read_excel('EURUSD=X_data_W1.xlsx', index_col='Date', parse_dates=True)

# Wczytanie danych dziennych z pliku Excel (SwissReAG_data_D1)
d1_data = pd.read_excel('EURUSD=X_data_D1.xlsx', index_col='Date', parse_dates=True)

# Przypisanie kolumn 'Median_6', 'BG' i 'BD' (banda dolna) z danych tygodniowych do danych dziennych
d1_data['Median_6'] = w1_data['Median_6'].reindex(d1_data.index, method='ffill')
d1_data['BG'] = w1_data['BG'].reindex(d1_data.index, method='ffill')
d1_data['BD'] = w1_data['BD'].reindex(d1_data.index, method='ffill')

# Tworzenie instancji Cerebro
cerebro = bt.Cerebro()


# Konwersja DataFrame na dane w formacie Backtrader z dodatkowymi liniami Median_6, BG i BD
class PandasDataExtended(bt.feeds.PandasData):
    lines = ('median_6', 'BG', 'BD')
    params = (
    ('datetime', None), ('open', -1), ('high', -1), ('low', -1), ('close', -1), ('volume', -1), ('openinterest', -1),
    ('median_6', -1), ('BG', -1), ('BD', -1))


data = PandasDataExtended(dataname=d1_data)

# Dodanie danych do Cerebro
cerebro.adddata(data)

# Dodanie strategii
cerebro.addstrategy(CustomStrategy)

# Dodanie analizatorów do statystyk
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")

# Ustawienie początkowego kapitału
cerebro.broker.setcash(10000.0)

# Uruchomienie backtestu z analizatorami
results = cerebro.run()

# Wyciąganie analizatorów z wyników
analyzers = results[0].analyzers

# Wyświetlanie podsumowania wyników
print_summary(analyzers)

# Wyświetlenie wykresu
cerebro.plot()
