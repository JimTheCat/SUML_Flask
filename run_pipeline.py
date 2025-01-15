import subprocess
import sys
import os

def install_requirements():
    """
    Instaluje zależności z pliku requirements.txt.
    """
    requirements_path = os.path.join(os.getcwd(), "requirements.txt")
    if os.path.exists(requirements_path):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
            print("Zależności zostały zainstalowane.")
        except subprocess.CalledProcessError as e:
            print(f"Błąd podczas instalacji zależności: {e}")
            exit(1)
    else:
        print("Plik requirements.txt nie został znaleziony.")

def run_script(script_path):
    """
    Uruchamia wskazany skrypt Python.
    """
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(f"Uruchomiono {script_path}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas uruchamiania {script_path}:\n{e.stderr}")
        exit(1)

if __name__ == "__main__":
    print("Rozpoczynanie pipeline...")

    # Krok 0: Instalacja zależności
    print("\nKrok 0: Instalacja zależności...")
    install_requirements()

    # Krok 1: Pobranie datasetu
    print("\nKrok 1: Pobieranie datasetu...")
    run_script("data/fetch_dataset.py")

    # Krok 2: Trening modelu
    print("\nKrok 2: Trening modelu...")
    run_script("src/model_training.py")

    # Informacja o zakończeniu
    print("\nPipeline zakończony. Możesz teraz uruchomić aplikację Flask:")
    print("python flask_app.py")
