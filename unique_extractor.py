﻿import os
from src.data_preprocessing import load_and_flatten_json, extract_unique_values

file_path = os.path.join(os.getcwd(), 'data/games.json')

df = load_and_flatten_json(file_path)

# Wykonanie one-hot encoding dla kolumn listowych
list_columns = ['categories', 'genres', 'estimated_owners']
extract_unique_values(df, list_columns)