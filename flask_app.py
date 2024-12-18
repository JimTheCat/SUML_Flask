from flask import Flask, request, jsonify, render_template, redirect, url_for
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Ładowanie wytrenowanego modelu
MODEL_PATH = 'model/random_forest_model.pkl'
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("Model załadowany pomyślnie.")
else:
    model = None
    print(f"Model nie został znaleziony pod ścieżką: {MODEL_PATH}")

# Funkcja do przygotowania danych wejściowych dla modelu
def prepare_data(input_data):
    """
    Konwertuje dane wejściowe na format używany przez model.
    W tym przykładzie uzupełniamy brakujące informacje domyślnymi wartościami.
    Docelowo powinieneś przekazywać wszystkie dane potrzebne do modelu.
    """
    data = {
        'peak_ccu': input_data.get('peak_ccu', 0),
        'price': input_data.get('price', 0.0),
        'dlc_count': input_data.get('dlc_count', 0),
        'positive': input_data.get('positive', 0),
        'negative': input_data.get('negative', 0),
        'average_playtime': input_data.get('average_playtime', 0),
        'required_age': input_data.get('required_age', 0),
        'metacritic_score': input_data.get('metacritic_score', 0),
        'user_score': input_data.get('user_score', 0),
        'achievements': input_data.get('achievements', 0),
        'recommendations': input_data.get('recommendations', 0),
        'average_playtime_2weeks': input_data.get('average_playtime_2weeks', 0),
        'languages': input_data.get('languages', ""),
        'developers': input_data.get('developers', ""),
        'publishers': input_data.get('publishers', ""),
        'genres': input_data.get('genres', ""),
        'categories': input_data.get('categories', ""),
        'tags': input_data.get('tags', "")
    }

    df = pd.DataFrame([data])
    return df

# Przykładowa "baza" gier (statyczna lista do demonstracji)
GAMES = [
    {"name": "Game1", "genre": "RPG", "price": 35, "score": 79, "copies_sold": 2123412},
    {"name": "Game2", "genre": "Action", "price": 50, "score": 82, "copies_sold": 1500000},
]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title="Home")

@app.route('/games')
def game_list():
    q = request.args.get('q')
    if q:
        filtered = [g for g in GAMES if q.lower() in g['name'].lower()]
    else:
        filtered = GAMES
    return render_template('game_list.html', games=filtered, title="Show All Games")

@app.route('/games/<game_name>')
def game_detail(game_name):
    game = next((g for g in GAMES if g['name'].lower() == game_name.lower()), None)
    if not game:
        return "Game not found", 404
    return render_template('game_detail.html', game=game, title=game['name'])

@app.route('/new', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        # Pobierz dane z formularza
        name = request.form.get('name')
        genre = request.form.get('genre')
        price_str = request.form.get('price', '0')
        try:
            price = float(price_str)
        except:
            price = 0.0

        # Budujemy input_data do modelu. W tym przykładzie wypełnimy resztę wartości domyślnie.
        input_data = {
            'peak_ccu': 100,       # przykładowa wartość domyślna
            'price': price,
            'dlc_count': 0,
            'positive': 1000,
            'negative': 100,
            'average_playtime': 50,
            'required_age': 0,
            'metacritic_score': 80,
            'user_score': 75,
            'achievements': 10,
            'recommendations': 500,
            'average_playtime_2weeks': 10,
            'languages': "English",
            'developers': "IndieDev",
            'publishers': "IndiePub",
            'genres': genre,
            'categories': "Single-player",
            'tags': "indie,action"
        }

        if model is None:
            return jsonify({'error': 'Model is not loaded!'}), 500

        data = prepare_data(input_data)
        prediction = model.predict(data)[0]

        return render_template('prediction_result.html', name=name, predicted=prediction, title="Prediction Result")

    return render_template('new_game_prediction.html', title="New Game Prediction")

# Opcjonalnie możesz zachować endpoint RESTowy /predict do integracji z zewnętrznymi narzędziami
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            input_data = request.json
            if not input_data:
                return jsonify({'error': 'Brak danych wejściowych'}), 400

            if model is None:
                return jsonify({'error': 'Model is not loaded!'}), 500

            data = prepare_data(input_data)
            prediction = model.predict(data)[0]
            return jsonify({'predicted_owners': int(prediction)})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
