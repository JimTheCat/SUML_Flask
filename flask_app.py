from flask import Flask, request, render_template
import pandas as pd
import test
import utils
import os
app = Flask(__name__)

genres = utils.open_from_file(os.path.join('unique_values', 'genres.txt'))
genres_2 = utils.open_from_file(os.path.join('unique_values', 'genres_2.txt'))
categories = utils.open_from_file(os.path.join('unique_values', 'categories.txt'))

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
        'metacritic_score': input_data.get('metacritic_score'),
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

    print(data)

    df = pd.DataFrame([data])
    return df

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title="Home")

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title="About Model")


def checkbox_to_bool(value_type):
    value_str = request.form.get(value_type)
    if value_str == 'on':
        value = 1
    else:
        value = 0
    return value

@app.route('/new', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':

        release_year = int(request.form.get('release_year'))
        release_month = int(request.form.get('release_month'))

        price = float(request.form.get('price'))
        dlc_count = int(request.form.get('dlc_count'))

        metacritic_score = int(request.form.get('metacritic_score'))
        positive = int(request.form.get('positive'))
        negative = int(request.form.get('negative'))

        windows = checkbox_to_bool('windows')
        mac = checkbox_to_bool('mac')
        linux = checkbox_to_bool('linux')

        selected_genres = request.form.getlist('genres')
        selected_categories = request.form.getlist('categories')

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
            'categories': selected_categories
        }

        data = prepare_data(input_data)
        prediction = test.predictor.predict(data).tolist()[0]

        return render_template('prediction_result.html', predicted=prediction, title="Prediction Result")

    return render_template('new_game_prediction.html', title="Game Sales Prediction", genres=genres_2,
                           categories=categories)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)
