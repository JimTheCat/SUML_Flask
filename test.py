from autogluon.tabular import TabularPredictor
import os

def find_latest_model(directory='AutogluonModels'):
    if not os.path.exists(directory):
        return None
    subdirs = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    if not subdirs:
        return None
    latest_model = max(subdirs, key=os.path.getmtime)  # Najnowszy katalog według daty modyfikacji
    return latest_model

# Funkcja do znalezienia najlepszego modelu na podstawie wyników walidacji
def find_best_model_by_name(directory='AutogluonModels', model_name=None):
    return directory if model_name is None else os.path.join(directory, model_name)

def get_best_model():
    path = find_latest_model(os.path.join(os.getcwd(), 'AutogluonModels'))
    model = TabularPredictor.load(path)
    ranking = model.leaderboard(silent=True)
    best = ranking.iloc[0]['model']
    return best

# Ścieżka do folderu z wynikami
save_path = find_latest_model(os.path.join(os.getcwd(), 'AutogluonModels'))

# Wczytaj model
predictor = TabularPredictor.load(save_path)

# Wyświetl ranking modeli
leaderboard = predictor.leaderboard(silent=True)
print(leaderboard)

# Najlepszy model (zwykle ten z najwyższym `score_val` dla wybranej metryki)
best_model = leaderboard.iloc[0]['model']
print(f"Najlepszy model: {best_model}")

# Usuń wszystkie modele poza najlepszym
predictor.delete_models(models_to_keep=[best_model], dry_run=False)

# Dry-run: Ustawienie na True pokaże, które modele zostałyby usunięte bez faktycznego usuwania

# Ścieżka do zapisu najlepszego modelu
best_model_path = find_best_model_by_name(os.path.join(os.getcwd(), 'AutogluonModels'), model_name=best_model)

print(f"Najlepszy model znajduje się w: {best_model_path}")