# Przewidywanie ilości sprzedanych kopii gier na platformie Steam

## Opis projektu

Celem projektu jest stworzenie modelu przewidującego ilość sprzedanych kopii gier na platformie Steam. W tym celu wykorzystane został dataset z [Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data).

## Opis danych

Dane zawierają informacje o grach dostępnych na platformie Steam. Zbiór zawiera 39 kolumn i ponad 97,000 gier. Kolumny zawierają informacje takie jak: nazwa gry, wydawca, ilość sprzedanych kopii, oceny, kategorie itd.

## Cel projektu

Celem projektu jest stworzenie modelu przewidującego ilość sprzedanych kopii gier na platformie Steam. 

## Jak uruchomić projekt w środowisku lokalnym?

1. Sklonuj repozytorium
2. Uruchom run_pipeline.py
3. Poczekaj na zakończenie działania skryptu, który automatycznie pobierze dane, przetworzy je i wytrenuje potrzebny model (może to zająć dłuższą chwile przez wzgląd na duży dataset)
4. Uruchom flask_app.py
5. Przejdź na strone http://localhost:5000/

## Autorzy

- Kazimierz Piontek, s24510

- Patryk Kłosiński, s25256

- Oskar Rojek, s25723
