import yfinance as yf

# Definicja tickeru dla Swiss Re AG
ticker = 'SREN.SW'

# Pobranie danych
sren_data = yf.download(ticker, start='2015-01-01', end='2024-09-21', interval='1d')

# Wyświetlenie pobranych danych
print(sren_data)

sren_data.to_csv('SwissRe_AG_History.csv')
