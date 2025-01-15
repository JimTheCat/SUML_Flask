# src/model_training.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor

# Funkcja do ładowania i przetwarzania danych
def load_data(file_path: str) -> pd.DataFrame:
    from data_preprocessing import load_and_flatten_json, one_hot_encode_list_columns, extract_unique_values

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
                       'median_playtime_2weeks', 'peak_ccu', 'tags', 'release_date', 'name', 'required_age']  # Dodaj inne kolumny, które nie są istotne
    df.drop(columns=columns_to_drop, axis=1, inplace=True)

    # Zamiana zakresu "estimated_owners" na średnią wartość
    df['estimated_owners'] = df['estimated_owners'].str.split(' - ').apply(
        lambda x: (int(x[0].replace(',', '')) + int(x[1].replace(',', ''))) // 2 if isinstance(x, list) else 0
    )

    # Wykonanie one-hot encoding dla kolumn listowych
    list_columns = ['supported_languages', 'full_audio_languages', 'categories', 'genres']
    extract_unique_values(df, list_columns)
    df = one_hot_encode_list_columns(df, list_columns)

    return df


# Ścieżka do pliku JSON
file_path = os.path.join(os.getcwd(), 'data/games.json')

# Wczytanie danych
print("Wczytywanie danych...")
df = load_data(file_path)
print("Dane wczytane i przetworzone.")

print(df.head())

# Przygotowanie cech (X) i etykiety (y)
X = df.drop('estimated_owners', axis=1)
y = df['estimated_owners']

# Podział danych na zestaw treningowy i testowy
X['estimated_owners'] = y  # AutoGluon wymaga, aby cel znajdował się w DataFrame
train_data, test_data = train_test_split(X, test_size=0.2, random_state=42)

# Trenowanie modelu za pomocą AutoGluon
print("Rozpoczęcie trenowania modelu za pomocą AutoGluon...")
predictor = TabularPredictor(label='estimated_owners', eval_metric='r2', problem_type='regression').fit(
    train_data=train_data,
    time_limit=600  # Ustaw limit czasu na trenowanie (w sekundach)
)
print("Model wytrenowany pomyślnie.")

print("Usuwanie zbędnych modeli...")

# Najlepszy model (zwykle ten z najwyższym `score_val` dla wybranej metryki)
leaderboard = predictor.leaderboard(silent=True)
best_model = leaderboard.iloc[0]['model']
print(f"Najlepszy model: {best_model}")

# Usuń wszystkie modele poza najlepszym
predictor.delete_models(models_to_keep=[best_model], dry_run=False)

print("Modele usunięte.")
