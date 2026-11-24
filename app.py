import json
import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'score.json')
CHOICES = ['rock', 'paper', 'scissors', 'lizard', 'spock']
BEATS = {
    'rock': ['scissors', 'lizard'],
    'paper': ['rock', 'spock'],
    'scissors': ['paper', 'lizard'],
    'lizard': ['paper', 'spock'],
    'spock': ['rock', 'scissors'],
}


def default_data():
    return {'user_score': 0, 'computer_score': 0,
            'counts': {c: 0 for c in CHOICES}}


def load_data():
    data = default_data()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                saved = json.load(f)
            data['user_score'] = saved.get('user_score', 0)
            data['computer_score'] = saved.get('computer_score', 0)
            data['counts'].update(saved.get('counts', {}))
        except (json.JSONDecodeError, OSError):
            pass
    return data


def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def favourite_choice():
    counts = data['counts']
    if sum(counts.values()) == 0:
        return None
    return max(counts, key=counts.get)


def determine_winner(user, computer):
    if user == computer:
        return 'draw'
    if computer in BEATS[user]:
        return 'win'
    return 'lose'


data = load_data()


@app.route('/')
def index():
    return render_template('index.html',
                           user_score=data['user_score'],
                           computer_score=data['computer_score'],
                           favourite=favourite_choice())


@app.route('/play', methods=['POST'])
def play():
    user_choice = request.json.get('choice')
    if user_choice not in CHOICES:
        return jsonify({'error': 'Invalid choice'}), 400

    computer_choice = random.choice(CHOICES)
    result = determine_winner(user_choice, computer_choice)

    data['counts'][user_choice] += 1
    if result == 'win':
        data['user_score'] += 1
    elif result == 'lose':
        data['computer_score'] += 1
    save_data()

    return jsonify({
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'result': result,
        'user_score': data['user_score'],
        'computer_score': data['computer_score'],
        'favourite': favourite_choice(),
    })


if __name__ == '__main__':
    app.run(debug=True)