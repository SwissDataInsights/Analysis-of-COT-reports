import pandas as pd

# Wczytywanie danych z pliku eur.csv
eur_csv_path = 'C:/COT/data_preparation/eur.csv'
df_eur = pd.read_csv(eur_csv_path)

# Upewnienie się, że kolumna daty jest typu datetime
df_eur['Report_Date_as_MM_DD_YYYY'] = pd.to_datetime(df_eur['Report_Date_as_MM_DD_YYYY'])

# Wczytywanie danych z pliku EURUSD=X.csv
eurusd_csv_path = 'C:/COT/data_preparation/EURUSD=X.csv'
df_eurusd = pd.read_csv(eurusd_csv_path)

# Upewnienie się, że kolumna daty jest typu datetime
df_eurusd['Date'] = pd.to_datetime(df_eurusd['Date'])

# Łączenie DataFrame'ów na podstawie daty
df_combined = pd.merge(df_eur, df_eurusd, left_on='Report_Date_as_MM_DD_YYYY', right_on='Date', how='left')

# Usunięcie zbędnej kolumny 'Date', jeśli chcesz zachować tylko jedną kolumnę z datą
df_combined = df_combined.drop(columns=['Date'])

# Zapis wyniku do nowego pliku CSV
output_csv_path = 'C:/COT/data_preparation/COT_EUR.csv'
df_combined.to_csv(output_csv_path, index=False)

print(f"Połączone dane zostały zapisane jako '{output_csv_path}'.")
