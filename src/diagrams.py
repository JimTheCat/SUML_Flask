import os

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Funkcja do generowania wykresów
def generate_visualizations(predictor, test_data):
    folder_path = "static/img"

    # Tworzenie folderów, jeśli nie istnieją
    os.makedirs(folder_path, exist_ok=True)

    leaderboard = predictor.leaderboard(silent=True)

    # 1. Macierz konfuzji
    print("Generowanie macierzy konfuzji...")
    y_true = test_data['estimated_owners']
    y_pred = predictor.predict(test_data.drop(columns=['estimated_owners']))
    conf_matrix = confusion_matrix(y_true, y_pred, labels=y_true.cat.categories)
    plt.figure(figsize=(12, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=y_true.cat.categories, yticklabels=y_true.cat.categories)
    plt.title("Macierz konfuzji")
    plt.xlabel("Predykcja")
    plt.ylabel("Rzeczywiste")
    plt.tight_layout()
    plt.savefig("static/img/confusion_matrix.png")
    plt.show()

    # 2. Feature Importance
    print("Generowanie ważności cech...")
    importance = predictor.feature_importance(test_data)

    print(importance.head())
    # Przenieś indeks do nowej kolumny 'feature'
    importance_reset = importance.reset_index()
    importance_reset.rename(columns={'index': 'feature'}, inplace=True)

    # Sortowanie według znaczenia
    importance_sorted = importance_reset.sort_values('importance', ascending=False)

    # Tworzenie wykresu
    plt.figure(figsize=(12, 8))
    sns.barplot(data=importance_sorted, x='importance', y='feature', palette='coolwarm')
    plt.title("Ważność cech")
    plt.xlabel("Znaczenie")
    plt.ylabel("Cechy")
    plt.tight_layout()
    plt.savefig("static/img/feature_importance.png")
    plt.show()

    # 3. Rozkład błędów klasyfikacji
    errors = y_pred != y_true

    plt.figure(figsize=(10, 6))
    sns.histplot(errors, kde=False, color='red')
    plt.title("Rozkład błędów klasyfikacji")
    plt.xlabel("Czy poprawne? (0 = poprawne, 1 = błędne)")
    plt.ylabel("Liczba próbek")
    plt.tight_layout()
    plt.savefig("static/img/error_distribution.png")
    plt.show()