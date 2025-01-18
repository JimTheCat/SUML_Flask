from flask import Flask, request, render_template
import pandas as pd
import test
import utils
import os
app = Flask(__name__)

genres = utils.open_from_file(os.path.join('unique_values', 'genres.txt'))
categories = utils.open_from_file(os.path.join('unique_values', 'categories.txt'))
original_languages = utils.open_from_file(os.path.join('unique_values', 'supported_languages.txt'))
languages = utils.open_from_file(os.path.join('unique_values', 'cleared_languages.txt'))
original_audio = utils.open_from_file(os.path.join('unique_values', 'full_audio_languages.txt'))
audio = utils.open_from_file(os.path.join('unique_values', 'cleared_audio.txt'))

# Funkcja do przygotowania danych wejściowych dla modelu
def prepare_data(input_data):
    """
    Konwertuje dane wejściowe na format używany przez model.
    """
    data = {
        'release_year' : input_data.get('release_year'),
        'release_month' : input_data.get('release_month'),
        'price': input_data.get('price'),
        'dlc_count': input_data.get('dlc_count'),
        'metacritic_score': input_data.get('metacritic_score', 0),
        'positive': input_data.get('positive'),
        'negative': input_data.get('negative'),
        'windows' : input_data.get('windows'),
        'mac' : input_data.get('mac'),
        'linux' : input_data.get('linux'),
    }

    for genre in genres:
        data[f"genres_{genre}"] = genre in input_data.get('genres')

    for category in categories:
        data[f"categories_{category}"] = category in input_data.get('categories')

    for language in original_languages:
        data[f"supported_languages_{language}"] = language in input_data.get('languages')

    for single_audio in original_audio:
        data[f"full_audio_languages_{single_audio}"] = single_audio in input_data.get('audio')

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

def string_to_float(value_type):
    value_str = request.form.get(value_type)
    try:
        value = float(value_str)
    except:
        value = 0
    return value


@app.route('/new', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':

        release_year = string_to_int(request.form.get('release_year'))
        release_month = string_to_int(request.form.get('release_month'))

        price = string_to_float(request.form.get('price'))
        dlc_count = string_to_int(request.form.get('dlc_count'))

        metacritic_score = string_to_int(request.form.get('metacritic_score'))
        positive = string_to_int(request.form.get('positive'))
        negative = string_to_int(request.form.get('negative'))

        windows = request.form.get('windows')
        mac = request.form.get('mac')
        linux = request.form.get('linux')

        selected_genres = request.form.getlist('genres')
        selected_categories = request.form.getlist('categories')
        selected_languages = request.form.getlist('languages')
        selected_audio = request.form.getlist("audio")

        print(selected_audio)

        input_data = {
            'release_year' : release_year,
            'release_month' : release_month,
            'price': price,
            'dlc_count': dlc_count,
            'metacritic_score': metacritic_score,
            'positive': positive,
            'negative': negative,
            'windows': windows,
            'mac': mac,
            'linux': linux,
            'genres': selected_genres,
            'categories': selected_categories,
            'languages': selected_languages,
            'audio' : selected_audio
        }

        data = prepare_data(input_data)
        prediction = test.predictor.predict(data)

        return render_template('prediction_result.html', predicted=prediction, title="Prediction Result")

    return render_template('new_game_prediction.html', title="New Game Prediction", genres=genres,
                           categories=categories, languages=languages, audio=audio)

if __name__ == '__main__':
    app.run(debug=True)
