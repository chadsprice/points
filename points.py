import flask
from flask import abort, jsonify, request

app = flask.Flask(__name__)
app.config['DEBUG'] = True

'''
points are organized by user -> date -> payer -> points

for example:

user_points = {
    'alice': {
        '2021-01-01': {
            'payer a': 100,
            'payer b': 200
        }
    }
}

'''
user_points = {}

@app.route('/add', methods=['GET'])
def add():
    json = request.get_json()
    user = json['user']
    # a better solution would be to use a JSON request validator package, but that would increase the number of dependencies and the configuration complexity, which is not necessary for this short example
    if not isinstance(user, str):
        abort(400, 'user must be string')
    date = json['date']
    if not isinstance(date, str):
        abort(400, 'date must be string')
    payer = json['payer']
    if not isinstance(payer, str):
        abort(400, 'payer must be string')
    points = json['points']
    if not isinstance(points, int):
        abort(400, 'points must be whole number')
    points = int(points)

    return handle_add(user, date, payer, points)

def handle_add(user, date, payer, points):
    if not user in user_points:
        user_points[user] = {}
    dates = user_points[user]

    if not date in dates:
        dates[date] = {}
    payers = dates[date]

    if not payer in payers:
        payers[payer] = 0

    if payers[payer] + points < 0:
        abort(400, 'would result in negative points for payer on given day')
    else:
        payers[payer] = payers[payer] + points

    return flask.Response(status=200)

@app.route('/balance', methods=['GET'])
def balance():
    json = request.get_json()
    user = json['user']
    if not isinstance(user, str):
        abort(400, 'user must be string')

    return handle_balance(user)

def handle_balance(user):
    balance = {}

    if user not in user_points:
        return jsonify(balance)

    for date in user_points[user].values():
        for payer, points in date.items():
            if payer not in balance:
                balance[payer] = 0
            balance[payer] = balance[payer] + points

    return jsonify(balance)

app.run()
