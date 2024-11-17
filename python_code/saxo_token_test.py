import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time

# Token autoryzacyjny
token = "eyJhbGciOiJFUzI1NiIsIng1dCI6IjI3RTlCOTAzRUNGMjExMDlBREU1RTVCOUVDMDgxNkI2QjQ5REEwRkEifQ.eyJvYWEiOiI3Nzc3NSIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiR1ZBbzJDdDg5Mkt3Q01DVVdpNXJqQT09IiwiY2lkIjoiR1ZBbzJDdDg5Mkt3Q01DVVdpNXJqQT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiOThhMjZmOTZmOWM0NDE4MDg2ZjAyZTgzOTYxZTE5YTciLCJkZ2kiOiI4NCIsImV4cCI6IjE3MzczMDYwMzQiLCJvYWwiOiIxRiIsImlpZCI6ImIzN2M4ZmQ2ZTJkOTQyOWQ3NGU2MDhkY2U5Zjc0N2FmIn0.ZOjZCt1pX6SCr0ijJcvJ1U7AsoVCiv3bQjc3EaIlT7wyiBF_Iq6BT2EsIJJB2vn_BHxhqE_ir1tM7z0qJ1cUyg"

# Nagłówki autoryzacyjne
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}


# Funkcja pobierająca dane historyczne
def get_historical_data(start_time):
    # Ustawienie URL z odpowiednimi parametrami dla interwału godzinnego (Horizon=60)
    #url = f"https://gateway.saxobank.com/sim/openapi/chart/v1/charts?AssetType=FxSpot&Horizon=60&Mode=From&Time={start_time}&Uic=21"
    url = f"https://gateway.saxobank.com/sim/openapi/chart/v1/charts?AssetType=Stock&Count=100&FieldGroups=BlockInfo&Horizon=1440&Mode=From&Time=2024-10-01&Uic=211"

    # Wysyłanie zapytania GET
    response = requests.get(url, headers=headers)

    # Sprawdzanie limitów z nagłówków
    if 'X-RateLimit-Session-Remaining' in response.headers:
        remaining_requests = int(response.headers['X-RateLimit-Session-Remaining'])
        reset_time = int(response.headers['X-RateLimit-Session-Reset'])

        print(f"Pozostało zapytań w sesji: {remaining_requests}, Reset za: {reset_time} sekund")

        if remaining_requests == 0:
            print(f"Osiągnięto limit zapytań. Oczekiwanie {reset_time} sekund na reset limitu.")
            time.sleep(reset_time + 1)  # Dodanie dodatkowej sekundy dla bezpieczeństwa

    # Sprawdzanie, czy odpowiedź jest poprawna
    if response.status_code == 200:
        data = response.json()["Data"]
        return data
    else:
        print(f"Błąd przy pobieraniu danych: {response.status_code}, {response.text}")
        return None


# Funkcja iterująca przez dane historyczne
def fetch_all_data(start_date):
    all_data = []
    current_time = start_date

    while True:
        print(f"Pobieranie danych od: {current_time}")
        data = get_historical_data(current_time)

        if not data:
            break  # Zakończ, jeśli brak danych

        # Dodanie danych do listy
        all_data.extend(data)

        # Zaktualizowanie czasu na podstawie ostatniego zwróconego rekordu
        last_time = data[-1]["Time"]
        current_time = datetime.strptime(last_time, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=1)
        current_time = current_time.strftime('%Y-%m-%dT%H:%M:%S')

        # Przerwanie, jeśli nie ma więcej danych
        if len(data) < 1200:
            break

    return all_data


# Początkowa data do pobierania danych
start_date = "2024-01-01T00:00:00"

# Pobieranie wszystkich danych
historical_data = fetch_all_data(start_date)

if historical_data:
    print(f"Dane pobrane pomyślnie. Zapisujemy do pliku Excel...")

    # Konwersja danych do DataFrame
    rows = []
    for item in historical_data:
        rows.append({
            "Time": item["Time"],
            "OpenBid": item["OpenBid"],
            "CloseBid": item["CloseBid"],
            "HighBid": item["HighBid"],
            "LowBid": item["LowBid"],
            "OpenAsk": item["OpenAsk"],
            "CloseAsk": item["CloseAsk"],
            "HighAsk": item["HighAsk"],
            "LowAsk": item["LowAsk"]
        })

    df = pd.DataFrame(rows)

    # Zapisanie do pliku Excel
    df.to_excel("EURUSD_data_historical_H1.xlsx", index=False)
    print("Dane zapisane w pliku 'EURUSD_data_historical_H1.xlsx'.")
