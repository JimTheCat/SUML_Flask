from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os
import test
app = Flask(__name__)

# Ładowanie wytrenowanego modelu
MODEL_PATH = test.best_model_path
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
        'release_year' : input_data.get('release_year'),
        'release_month' : input_data.get('release_month'),
        # 'peak_ccu': input_data.get('peak_ccu', 0),
        # 'price': input_data.get('price', 0.0),
        # 'dlc_count': input_data.get('dlc_count', 0),
        # 'positive': input_data.get('positive', 0),
        # 'negative': input_data.get('negative', 0),
        # 'average_playtime': input_data.get('average_playtime', 0),
        # 'required_age': input_data.get('required_age', 0),
        # 'metacritic_score': input_data.get('metacritic_score', 0),
        # 'user_score': input_data.get('user_score', 0),
        # 'achievements': input_data.get('achievements', 0),
        # 'recommendations': input_data.get('recommendations', 0),
        # 'average_playtime_2weeks': input_data.get('average_playtime_2weeks', 0),
        # 'languages': input_data.get('languages', ""),
        # 'developers': input_data.get('developers', ""),
        # 'publishers': input_data.get('publishers', ""),
        # 'genres': input_data.get('genres', ""),
        # 'categories': input_data.get('categories', ""),
        # 'tags': input_data.get('tags', "")
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


def string_to_int(value_type):
    value_str = request.form.get(value_type)
    try:
        value = int(value_str)
    except:
        value = 0
    return value

@app.route('/new', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        # Pobierz dane z formularza
        release_year = string_to_int(request.form.get('release_year'))
        release_month = string_to_int(request.form.get('release_month'))

        name = request.form.get('name')
        genre = request.form.get('genre')
        language = request.form.get('languages')
        developer = request.form.get('developers')
        publisher = request.form.get('publishers')
        category = request.form.get('categories')
        tag = request.form.get('tags')

        peak_ccu_str = request.form.get('peak_ccu', '0')
        try:
            peak_ccu = int(peak_ccu_str)
        except:
            peak_ccu = 0

        dlc_count_str = request.form.get('dlc_count', '0')
        try:
            dlc_count = int(dlc_count_str)
        except:
            dlc_count = 0

        price_str = request.form.get('price', '0')
        try:
            price = float(price_str)
        except:
            price = 0.0

        positive_str = request.form.get('positive', '0')
        try:
            positive = int(positive_str)
        except:
            positive = 0

        negative_str = request.form.get('negative', '0')
        try:
            negative = int(negative_str)
        except:
            negative = 0

        average_playtime_str = request.form.get('average_playtime', '0')
        try:
            average_playtime = int(average_playtime_str)
        except:
            average_playtime = 0

        required_age_str = request.form.get('required_age', '0')
        try:
            required_age = int(required_age_str)
        except:
            required_age = 0

        metacritic_score_str = request.form.get('metacritic_score', '0')
        try:
            metacritic_score = int(metacritic_score_str)
        except:
            metacritic_score = 0

        user_score_str = request.form.get('user_score', '0')
        try:
            user_score = int(user_score_str)
        except:
            user_score = 0

        achievements_str = request.form.get('achievements', '0')
        try:
            achievements = int(achievements_str)
        except:
            achievements = 0

        recommendations_str = request.form.get('recommendations', '0')
        try:
            recommendations = int(recommendations_str)
        except:
            recommendations = 0

        average_playtime_2weeks_str = request.form.get('average_playtime_2weeks', '0')
        try:
            average_playtime_2weeks = int(average_playtime_2weeks_str)
        except:
            average_playtime_2weeks = 0

        # Budujemy input_data do modelu. W tym przykładzie wypełnimy resztę wartości domyślnie.
        input_data = {
            'release_year' : release_year,
            'release_month' : release_month,
            # 'peak_ccu': peak_ccu,
            # 'price': price,
            # 'dlc_count': dlc_count,
            # 'positive': positive,
            # 'negative': negative,
            # 'average_playtime': average_playtime,
            # 'required_age': required_age,
            # 'metacritic_score': metacritic_score,
            # 'user_score': user_score,
            # 'achievements': achievements,
            # 'recommendations': recommendations,
            # 'average_playtime_2weeks': average_playtime_2weeks,
            # 'languages': language,
            # 'developers': developer,
            # 'publishers': publisher,
            # 'genres': genre,
            # 'categories': category,
            # 'tags': tag
        }

        if model is None:
            return jsonify({'error': 'Model is not loaded!'}), 500

        data = prepare_data(input_data)
        prediction = model.predict(data)

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
