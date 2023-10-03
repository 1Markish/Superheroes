from random import randint, choice as rc, sample
from faker import Faker
from app import app
from models import db, Hero, Power, Hero_powers

power_data = [
  {"name":"super strength" , "description" : "gives the wielder super-human strengths"},
  {"name":" flight" , "description" : "gives the wielder the ability to fly through the skies at supersonic speed"},
  {"name":" super human senses" , "description" : "allows the wielder to use her senses at a super-human level"},
  {"name":" elasticity" , "description" : "can stretch the human body to extreme lengths"}
]

hero_data = [
  {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
  { "name": "Doreen Green", "super_name": "Squirrel Girl" },
  { "name": "Gwen Stacy","super_name": "Spider-Gwen" },
  { "name": "Janet Van Dyne","super_name": "The Wasp" },
  { "name": "Wanda Maximoff","super_name": "Scarlet Witch" },
  { "name": "Carol Danvers","super_name": "Captain Marvel" },
  { "name": "Jean Grey","super_name": "Dark Phoenix" },
  { "name": "Ororo Munroe","super_name": "Storm" },
  { "name": "Kitty Pryde","super_name": "Shadowcat" },
  { "name": "Elektra Natchios", "super_name": "Elektra" }
]


strengths = ["Strong", "Weak", "Average"]


fake = Faker()


with app.app_context():
  
  db.session.query(Hero).delete()
  db.session.query(Hero_powers).delete()
  db.session.query(Power).delete()
  
  heros = []
  for i in hero_data:
    h = Hero(
      name = i["name"] , 
      super_name = i["super_name"]
    )
    heros.append(h)
    
  db.session.add_all(heros)
  db.session.commit()
  
  powers = []
  for i in power_data:
    p = Power(
      name = i['name'],
      description = i["description"]
    )
    powers.append(p)
  
  db.session.add_all(powers)
  db.session.commit()
  
  hero_powers = []
  for i in strengths:
    hp = Hero_powers(
      strength = rc(strengths)
    )
    hero_powers.append(hp)
    
  db.session.add_all(hero_powers)
  db.session.commit()
  
  
    
    