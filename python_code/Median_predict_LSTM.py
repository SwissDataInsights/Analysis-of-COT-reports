# Importowanie wymaganych bibliotek
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import xgboost as xgb
from imblearn.over_sampling import SMOTE
from collections import Counter
from scipy.stats import randint, uniform
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytaj dane
data = pd.read_excel('SwissReAG_data_D1.xlsx')  # Plik SwissReAG z RSI i medianą

# Dodanie cech bezpośrednio związanych z ceną zamknięcia, zmiennością, różnicą cen i wolumenem
data['Price_Diff'] = data['Close'].diff()  # Różnica między dniami
data['Volatility'] = data['Close'].rolling(window=10).std()  # 10-okresowa zmienność (odchylenie standardowe)

# Usuwamy brakujące wartości
data.dropna(inplace=True)

# Skupiamy się na cechach: Close, Price_Diff, Volatility, Volume
features = data[['Close', 'Price_Diff', 'Volatility', 'Volume']]

# Tworzenie celu: 1, jeśli cena zamknięcia jest powyżej mediany 6-dniowej, inaczej 0
data['Above_Median'] = np.where(data['Close'] > data['Median_6'], 1, 0)
target = data['Above_Median']

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)

# Zrównoważenie klas za pomocą SMOTE
sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

# Sprawdź zbalansowanie po SMOTE
print(f"Rozkład po zastosowaniu SMOTE: {Counter(y_train_res)}")

# Skalowanie danych
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test)

# Definicja modelu XGBoost
xgb_model = xgb.XGBClassifier(
    random_state=42,
    eval_metric='logloss'  # Metryka oceny
)

# Definicja przestrzeni przeszukiwania parametrów dla RandomizedSearchCV
param_distributions = {
    'n_estimators': randint(50, 1000),  # Liczba estymatorów
    'learning_rate': uniform(0.01, 0.5),  # Szybkość uczenia
    'max_depth': randint(3, 12),  # Głębokość drzewa
    'subsample': uniform(0.5, 0.5),  # Współczynnik próbkowania
    'colsample_bytree': uniform(0.5, 0.5),  # Współczynnik próbkowania kolumn
    'gamma': uniform(0, 5),  # Parametr gamma
    'min_child_weight': randint(1, 6)  # Parametr min_child_weight
}

# RandomizedSearchCV z F1 Score jako metryką
random_search = RandomizedSearchCV(
    estimator=xgb_model,
    param_distributions=param_distributions,
    n_iter=100,  # Liczba losowych wyszukiwań
    scoring='f1',  # Używamy F1 jako metryki
    cv=5,  # Walidacja krzyżowa
    verbose=1,
    n_jobs=-1,
    random_state=42  # Stałość wyników
)

# Trenowanie RandomizedSearchCV
random_search.fit(X_train_scaled, y_train_res)

# Wyświetlenie najlepszych parametrów
print(f"Najlepsze parametry: {random_search.best_params_}")

# Przewidywanie na danych testowych z najlepszym modelem
best_model = random_search.best_estimator_
xgb_predictions = best_model.predict(X_test_scaled)

# Obliczanie dokładności i F1 score
xgb_accuracy = accuracy_score(y_test, xgb_predictions)
xgb_f1 = f1_score(y_test, xgb_predictions)

# Wyświetlenie wyników
print(f'Dokładność modelu Gradient Boosting (XGBoost): {xgb_accuracy * 100:.2f}%')
print(f'F1 Score modelu Gradient Boosting (XGBoost): {xgb_f1:.2f}')

# Wyświetlenie raportu klasyfikacji
print("\nRaport klasyfikacji:")
print(classification_report(y_test, xgb_predictions, target_names=['Poniżej Mediany', 'Powyżej Mediany']))

# Rysowanie macierzy pomyłek
cm = confusion_matrix(y_test, xgb_predictions)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Poniżej Mediany', 'Powyżej Mediany'], yticklabels=['Poniżej Mediany', 'Powyżej Mediany'])
plt.ylabel('Rzeczywiste')
plt.xlabel('Przewidywane')
plt.title('Macierz pomyłek')
plt.show()

# Analiza reszt błędów
residuals = y_test - xgb_predictions

# Rysowanie wykresu reszt błędów
plt.figure(figsize=(10, 6))
plt.hist(residuals, bins=20, edgecolor='black')
plt.title('Rozkład reszt błędów')
plt.xlabel('Reszty')
plt.ylabel('Liczba obserwacji')
plt.show()

# Wyświetlenie reszt dla bardziej szczegółowej analizy
plt.figure(figsize=(10, 6))
plt.scatter(range(len(residuals)), residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.title('Wykres reszt błędów')
plt.xlabel('Indeks')
plt.ylabel('Reszta')
plt.show()
