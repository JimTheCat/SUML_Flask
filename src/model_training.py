# src/model_training.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor

from src.diagrams import generate_visualizations


# Funkcja do ładowania i przetwarzania danych
def load_data(file_path: str) -> pd.DataFrame:
    from data_preprocessing import load_and_flatten_json, one_hot_encode_list_columns

    # Wczytanie i przetworzenie danych
    df = load_and_flatten_json(file_path)

    # Konwersja release_date na datetime i wyodrębnienie roku i miesiąca
    df['release_date'] = pd.to_datetime(df['release_date'], format='%b %d, %Y', errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    df['release_month'] = df['release_date'].dt.month

    # Filtracja nieistotnych kolumn
    columns_to_drop = ['detailed_description', 'about_the_game', 'short_description', 'reviews', 'header_image',
                       'website', 'support_url', 'support_email', 'metacritic_url', 'achievements', 'recommendations',
                       'notes', 'packages', 'developers', 'publishers', 'screenshots', 'movies', 'user_score',
                       'score_rank', 'average_playtime_forever', 'average_playtime_2weeks', 'median_playtime_forever',
                       'median_playtime_2weeks', 'peak_ccu', 'tags', 'release_date', 'name', 'required_age',
                       'supported_languages', 'full_audio_languages']
    df.drop(columns=columns_to_drop, axis=1, inplace=True)

    # Zamiana zakresów "estimated_owners" na klasy
    df = transform_estimated_owners(df)

    # Wykonanie one-hot encoding dla kolumn listowych
    list_columns = ['categories', 'genres']
    df = one_hot_encode_list_columns(df, list_columns)

    return df

# Funkcja do przekształcenia kolumny estimated_owners w klasy
def transform_estimated_owners(df):
    # Definicja przedziałów i etykiet klas
    bins = [0, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000, 20000000, 50000000, 100000000, 200000000]
    labels = [
        "0-20k", "20k-50k", "50k-100k", "100k-200k", "200k-500k",
        "500k-1M", "1M-2M", "2M-5M", "5M-10M", "10M-20M",
        "20M-50M", "50M-100M", "100M-200M"
    ]

    # Rozbijanie zakresów i zamiana na wartości średnie
    df['estimated_owners'] = df['estimated_owners'].str.split(' - ').apply(
        lambda x: (int(x[0].replace(',', '')) + int(x[1].replace(',', ''))) // 2 if isinstance(x, list) else 0
    )
    # Przypisywanie do klas
    df['estimated_owners'] = pd.cut(df['estimated_owners'], bins=bins, labels=labels, include_lowest=True)
    return df

# Ścieżka do pliku JSON
file_path = os.path.join(os.getcwd(), 'data/games.json')

# Wczytanie danych
print("Wczytywanie danych...")
df = load_data(file_path)
print("Dane wczytane i przetworzone.")

# Przygotowanie cech (X) i etykiety (y)
X = df.drop('estimated_owners', axis=1)
y = df['estimated_owners']

# Podział danych na zestaw treningowy i testowy
X['estimated_owners'] = y  # AutoGluon wymaga, aby cel znajdował się w DataFrame
train_data, test_data = train_test_split(X, test_size=0.2, random_state=42)

# Trenowanie modelu za pomocą AutoGluon
print("Rozpoczęcie trenowania modelu za pomocą AutoGluon...")
predictor = TabularPredictor(label='estimated_owners', eval_metric='accuracy', problem_type='multiclass').fit(
    train_data=train_data,
    time_limit=700  # Ustaw limit czasu na trenowanie (w sekundach)
)
print("Model wytrenowany pomyślnie.")

print("Usuwanie zbędnych modeli...")

# Najlepszy model (zwykle ten z najwyższym `score_val` dla wybranej metryki)
leaderboard = predictor.leaderboard(silent=True)

# Jeśli najlepszy model to WeightedEnsemble_L2 lub ExtraTreesMSE, wybierz drugi najlepszy
if leaderboard.iloc[0]['model'] == 'WeightedEnsemble_L2' or leaderboard.iloc[0]['model'] == 'ExtraTreesMSE':
    best_model = leaderboard.iloc[1]['model']
else:
    best_model = leaderboard.iloc[0]['model']

print(f"Najlepszy model: {best_model}")

# Usuń wszystkie modele poza najlepszym
predictor.delete_models(models_to_keep=[best_model], dry_run=False)

print("Modele usunięte.")

print("Generowanie diagramów...")
generate_visualizations(predictor, test_data)
print("Diagramy wygenerowane.")
