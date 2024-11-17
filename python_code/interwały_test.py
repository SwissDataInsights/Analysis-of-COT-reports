import requests

# Ogólne zapytanie bez dodatkowych filtrów
url = "https://gateway.saxobank.com/sim/openapi/ref/v1/instruments"
headers = {
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsIng1dCI6IjI3RTlCOTAzRUNGMjExMDlBREU1RTVCOUVDMDgxNkI2QjQ5REEwRkEifQ.eyJvYWEiOiI3Nzc3NSIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiR1ZBbzJDdDg5Mkt3Q01DVVdpNXJqQT09IiwiY2lkIjoiR1ZBbzJDdDg5Mkt3Q01DVVdpNXJqQT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiY2M4YTNiOWZkNTA3NDQ5MWI2NjIyYzczYzZlYzAxZTQiLCJkZ2kiOiI4NCIsImV4cCI6IjE3MzcxODY2MTUiLCJvYWwiOiIxRiIsImlpZCI6ImIzN2M4ZmQ2ZTJkOTQyOWQ3NGU2MDhkY2U5Zjc0N2FmIn0.EzUKvYLWU9VMsda91Zgh5lmiXygDy7C1GFVMLTdHCdW3hIW3MmHkOd1AtHAl3hV5H7lfdNagDqYpoAzeCiYrGQ',
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)

# Sprawdzenie kodu odpowiedzi
if response.status_code == 200:
    try:
        print(response.json())  # Próbujemy odczytać odpowiedź jako JSON
    except requests.exceptions.JSONDecodeError:
        print("Nie udało się odczytać odpowiedzi jako JSON. Odpowiedź serwera:")
        print(response.text)  # Wyświetl pełną odpowiedź serwera dla diagnostyki
else:
    print(f"Błąd {response.status_code}. Szczegóły: {response.text}")
