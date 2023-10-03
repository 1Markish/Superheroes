#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
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
        "message": "WELCOME TO THE PIZZA RESTAURANT API."
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

# get powers
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


# create hero power relationship
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    # Validate that the required fields are present in the request
    required_fields = ["strength", "power_id", "hero_id"]
    if not all(key in data for key in required_fields):
        return make_response(jsonify({"errors": ["Validation errors"]}), 400)

    # Check if the Hero and Power exist
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])

    if not hero or not power:
        return make_response(jsonify({"errors": ["Validation errors"]}), 400)

    # Create a new Hero_powers
    hero_power = Hero_powers(
        strength=data["strength"],
        hero_id=data["hero_id"],
        power_id=data["power_id"]
    )

    db.session.add(hero_power)
    db.session.commit()

    hero_data = {
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
    return make_response(jsonify(hero_data), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
