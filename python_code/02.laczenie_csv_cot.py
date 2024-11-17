import os
import requests
import zipfile
import pandas as pd

# URL-e do plików ZIP
urls = {
    'annual_2020': 'https://www.cftc.gov/files/dea/history/dea_fut_xls_2020.zip',
    'annual_2021': 'https://www.cftc.gov/files/dea/history/dea_fut_xls_2021.zip',
    'annual_2022': 'https://www.cftc.gov/files/dea/history/dea_fut_xls_2022.zip',
    'annual_2023': 'https://www.cftc.gov/files/dea/history/dea_fut_xls_2023.zip',
    'annual_2024': 'https://www.cftc.gov/files/dea/history/dea_fut_xls_2024.zip'
}

extracted_dir = 'C:/COT/data_preparation'

# Tworzenie katalogu, jeśli nie istnieje
os.makedirs(extracted_dir, exist_ok=True)

# Pobieranie i rozpakowywanie plików ZIP
for name, url in urls.items():
    zip_file_path = f'{name}.zip'

    # Pobieranie pliku ZIP
    response = requests.get(url)
    response.raise_for_status()
    with open(zip_file_path, 'wb') as file:
        file.write(response.content)

    # Rozpakowywanie pliku ZIP
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            if filename:
                # Utworzenie pełnej ścieżki do zapisu pliku
                extracted_file_path = os.path.join(extracted_dir, f'{name}_{filename}')
                with zip_ref.open(member) as source, open(extracted_file_path, 'wb') as target:
                    target.write(source.read())

    # Usunięcie pobranego pliku ZIP po rozpakowaniu
    os.remove(zip_file_path)

# Wczytywanie rozpakowanych plików Excel do DataFrame'ów pandas
dfs = []
for file in os.listdir(extracted_dir):
    if file.endswith('.xls'):
        file_path = os.path.join(extracted_dir, file)
        df = pd.read_excel(file_path)
        dfs.append(df)

# Łączenie wszystkich DataFrame'ów w jeden
combined_df = pd.concat(dfs, ignore_index=True)

# Ścieżka do zapisu wynikowego pliku CSV
output_csv_path = 'C:/COT/data_preparation/combined_data.csv'

# Zapisywanie połączonego DataFrame do pliku CSV
combined_df.to_csv(output_csv_path, index=False)

print(f"Pliki zostały pobrane, połączone i zapisane jako '{output_csv_path}'.")
