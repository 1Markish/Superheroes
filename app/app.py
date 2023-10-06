#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response, abort
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound

from models import db, Hero, Power, Hero_powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)

# create a response for landing page
@app.route('/')
def home():
    response_message = {
        "message": "WELCOME TO THE HEROS API."
    }
    return make_response(jsonify(response_message), 200)


# get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        heroes.append(hero_dict)
    return make_response(jsonify(heroes), 200)


# get hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.filter_by(id=id).first()
    if hero:
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description,
                }
                for hero_power in hero.powers
            ]
        }
        return make_response(jsonify(hero_dict), 200)
    else:
        return make_response(jsonify({"error": "Hero not found"}), 404)

# get powers.
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = []
    for power in Power.query.all():
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        powers.append(power_dict)
    return make_response(jsonify(powers), 200)



# get power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if power:
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        return make_response(jsonify(power_dict), 200)
    else:
        return make_response(jsonify({"error": "Power not found"}), 404)


# update power by ID
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    data = request.get_json()
    if power:
        for attr in data:
            setattr(power, attr, data[attr])

        db.session.add(power)
        db.session.commit()
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        return make_response(jsonify(power_dict), 200)
    else:
        return make_response(jsonify({"error": "Power not found"}), 404)



@app.route('/hero_powers', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data, expected JSON"}), 400

    member = Hero_powers(
        id=data.get('id'),
        strength=data.get('strength')
    )

    db.session.add(member)
    db.session.commit()

    return jsonify({"message": "Member signed up successfully"}), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
