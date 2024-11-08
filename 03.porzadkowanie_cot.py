import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ścieżka do pliku CSV
csv_file_path = 'C:/COT/data_preparation/combined_data.csv'

# Wczytywanie danych z pliku CSV do DataFrame
df = pd.read_csv(csv_file_path)

# Znalezienie indeksu kolumny 'NonRept_Positions_Short_All'
col_index = df.columns.get_loc('NonRept_Positions_Short_All')

# Zatrzymanie tylko kolumn do indeksu 'NonRept_Positions_Short_All' włącznie
df = df.iloc[:, :col_index + 1]

# Lista kolumn do usunięcia
kolumny_do_usuniecia = [
    'As_of_Date_In_Form_YYMMDD',
    'Open_Interest_All',
    'NonComm_Postions_Spread_All',
    'CFTC_Contract_Market_Code',
    'CFTC_Market_Code',
    'CFTC_Region_Code',
    'CFTC_Commodity_Code',
    'Tot_Rept_Positions_Long_All',
    'Tot_Rept_Positions_Short_All'
]

# Usuwanie kolumn, które istnieją w DataFrame
kolumny_do_usuniecia = [kol for kol in kolumny_do_usuniecia if kol in df.columns]
df = df.drop(columns=kolumny_do_usuniecia)

# Dodawanie kolumn z różnicami
df['Difference_NonComm'] = df['NonComm_Positions_Long_All'] - df['NonComm_Positions_Short_All']
df['Difference_Comm'] = df['Comm_Positions_Long_All'] - df['Comm_Positions_Short_All']
df['Difference_NonRept'] = df['NonRept_Positions_Long_All'] - df['NonRept_Positions_Short_All']

df['Sum_NonComm'] = df['NonComm_Positions_Long_All'] + df['NonComm_Positions_Short_All']
df['Sum_Comm'] = df['Comm_Positions_Long_All'] + df['Comm_Positions_Short_All']
df['Sum_NonRept'] = df['NonRept_Positions_Long_All'] + df['NonRept_Positions_Short_All']

df['L%_NonComm'] = df['NonComm_Positions_Long_All'] / df['Sum_NonComm']
df['L%_Comm'] = df['Comm_Positions_Long_All'] / df['Sum_Comm']
df['L%_NonRept'] = df['NonRept_Positions_Long_All'] / df['Sum_NonRept']

df_eur = df[df['Market_and_Exchange_Names'] == 'EURO FX - CHICAGO MERCANTILE EXCHANGE']

# Sortowanie DataFrame według daty
df_eur = df_eur.sort_values(by='Report_Date_as_MM_DD_YYYY')

# Wyświetlanie wykresu liniowego
plt.figure(figsize=(12, 6))
plt.plot(df_eur['Report_Date_as_MM_DD_YYYY'], df_eur['L%_NonComm'], label='L%_NonComm')
plt.plot(df_eur['Report_Date_as_MM_DD_YYYY'], df_eur['L%_Comm'], label='L%_Comm')
plt.plot(df_eur['Report_Date_as_MM_DD_YYYY'], df_eur['L%_NonRept'], label='L%_NonRept')
plt.xlabel('Data')
plt.ylabel('Wartość')
plt.title('Procentowe wartości pozycji dla EURO FX - CHICAGO MERCANTILE EXCHANGE')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Zapis zmodyfikowanego DataFrame do pliku CSV
output_csv_path = 'C:/COT/data_preparation/eur.csv'
df_eur.to_csv(output_csv_path, index=False)