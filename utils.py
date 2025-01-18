def open_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        extracted_list = [line.strip() for line in lines if line.strip()]

        return extracted_list
    except FileNotFoundError:
        print(f"Błąd: Plik {path} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")