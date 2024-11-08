import requests
import json
import pandas as pd
import datetime

# Token autoryzacyjny
token = "eyJhbGciOiJFUzI1NiIsIng1dCI6IjI3RTlCOTAzRUNGMjExMDlBREU1RTVCOUVDMDgxNkI2QjQ5REEwRkEifQ.eyJvYWEiOiI3Nzc3NSIsImlzcyI6Im9hIiwiYWlkIjoiR1ZBbzJDdDg5Mkt3Q01DVVdpNXJqQT09IiwiY2lkIjoiR1ZBbzJDdDg5Mkt3Q01DVVdpNXJqQT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiNzg4YzNmNzQ2ZjVkNGEzZjhhZmMyYTg0MGQxNjUzM2EiLCJkZ2kiOiI4NCIsImV4cCI6IjE3MzcxOTUxMzAiLCJvYWwiOiIxRiIsImlpZCI6ImIzN2M4ZmQ2ZTJkOTQyOWQ3NGU2MDhkY2U5Zjc0N2FmIn0.597gLGpmjoyynM1ZWdU_yoweA1kEw59oAmREVy5bq4iXMDgq2e5GSL_QBZcIUfnLSGaPWwybFFpZmqg5tG-eQA"

# Nagłówki autoryzacyjne
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}


# Funkcja do pobierania danych w partiach
def fetch_data(start_date, end_date, uic=21, asset_type='FxSpot', horizon=1, count=1200):
    start_time_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://gateway.saxobank.com/sim/openapi/chart/v1/charts?AssetType={asset_type}&Horizon={horizon}&Uic={uic}&StartTime={start_time_str}&EndTime={end_time_str}&Count={count}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(
            f"Pobrano dane od {start_time_str} do {end_time_str}. Liczba rekordów: {len(response.json().get('Data', []))}")
        return response.json().get("Data", [])
    else:
        print(f"Błąd przy pobieraniu danych: {response.status_code}, {response.text}")
        return []


# Ustawienia zakresu czasowego (ostatnie dwa dni)
end_date = datetime.datetime.utcnow()
start_date = end_date - datetime.timedelta(days=2)

# Pobieranie danych w partiach, ponieważ limit wynosi 1200 próbek
all_data = []
current_end_date = end_date

while start_date < current_end_date:
    data = fetch_data(start_date, current_end_date)
    if not data:
        break
    all_data.extend(data)
    # Zmiana current_end_date na ostatnią pobraną próbkę (Time) w celu pobrania wcześniejszych danych
    last_time = data[-1]["Time"]
    print(f"Ostatnia pobrana próbka ma czas: {last_time}")
    current_end_date = datetime.datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%SZ")

# Sprawdzanie, czy dane zostały pobrane
if all_data:
    # Konwersja danych do DataFrame
    rows = []
    for item in all_data:
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
    df.to_excel("eurusd_data_last_two_days.xlsx", index=False)
    print("Dane zapisane w pliku 'eurusd_data_last_two_days.xlsx'.")
else:
    print("Brak pobranych danych.")
