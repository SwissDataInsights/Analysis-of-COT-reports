import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE

# Ścieżka do pliku CSV
csv_file_path = 'C:/COT/data_preparation/COT_EUR.csv'

# Wczytywanie danych z pliku CSV
df = pd.read_csv(csv_file_path)

# Wyświetlanie nazw kolumn
print("Nazwy kolumn w pliku CSV:")
print(df.columns)

# Upewnienie się, że kolumna daty jest typu datetime
df['Report_Date_as_MM_DD_YYYY'] = pd.to_datetime(df['Report_Date_as_MM_DD_YYYY'])

# Tworzenie kolumny z kierunkiem ruchu kursu na najbliższy tydzień
df['Next_Week_Close'] = df['Close'].shift(-1)
df = df.dropna()
df['Direction'] = np.where(df['Next_Week_Close'] > df['Close'], 1, 0)

# Tworzenie dodatkowych cech (różnica w wartościach zamknięcia z poprzednich tygodni)
df['Prev_Week_Close'] = df['Close'].shift(1)
df['Change_Close'] = df['Close'] - df['Prev_Week_Close']
df = df.dropna()

# Wybór cech i etykiet
features = df[['L%_NonComm', 'L%_Comm', 'L%_NonRept', 'Close', 'Change_Close']]
labels = df['Direction']

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42, shuffle=False)

# Balansowanie zbioru treningowego
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Skalowanie danych
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Przekształcenie danych do kształtu wymaganego przez LSTM
X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# Funkcja do budowy modelu LSTM
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Budowa i trenowanie modelu
model = build_model()
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Ewaluacja modelu
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Prognozowanie kierunku ruchu kursu
predictions = model.predict(X_test)
predictions = (predictions > 0.5).astype(int)

# Wyświetlanie pierwszych kilku prognozowanych i rzeczywistych wartości
print("Predykcje:", predictions[:10].flatten())
print("Rzeczywiste:", y_test.values[:10])
