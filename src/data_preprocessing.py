import pandas as pd
import os

# Funkcja do wczytania i spłaszczenia JSON-a
def load_and_flatten_json(file_path: str) -> pd.DataFrame:
    data = pd.read_json(file_path).T
    return data

# Funkcja do wyciągania unikalnych wartości
def extract_unique_values(df: pd.DataFrame, list_columns: list):
    unique_values = {}
    os.makedirs('unique_values', exist_ok=True)
    for col in list_columns:
        unique_values[col] = df[col].explode().dropna().unique().tolist()
        with open(f'unique_values/{col}.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(map(str, unique_values[col])))

# Funkcja do one-hot encoding kolumn listowych
def one_hot_encode_list_columns(df: pd.DataFrame, list_columns: list) -> pd.DataFrame:
    for col in list_columns:
        df = df.join(df[col].explode().str.get_dummies().groupby(level=0).max().add_prefix(f'{col}_'))
        df.drop(columns=[col], inplace=True)
    return df
