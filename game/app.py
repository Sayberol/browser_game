from functools import wraps
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for

from game.characters import character_classes
from game.equipment import EquipmentData
from game.hero import Player, Hero, Enemy
from game.implement_project import Game
from game.utils import load_equipment

app = Flask(__name__)
app.url_map.strict_slashes = False
RESULT: EquipmentData = load_equipment()

heroes: Dict[str, Hero] = dict()

game = Game()


def game_processing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if game.game_processing:
            return func(*args, **kwargs)
        if game.game_results:
            return render_template('fight.html', heroes=heroes, result=game.game_results)
        return redirect(url_for('index'))
    return wrapper


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/choose-hero', methods=['GET', 'POST'])
def choose_hero():
    if request.method == 'GET':
        return render_template(
            'hero_choosing.html',
            result= {
                "header": "Выберите бойца",
                "classes": character_classes,
                "weapons": RESULT.get_weapon_names,
                "armors": RESULT.get_armor_names,
            }
        )
    heroes['player'] = Player(
        unit_class=character_classes[request.form['unit_class']],
        weapon=load_equipment().get_weapon(request.form['weapon']),
        armor=load_equipment().get_armor(request.form['armor']),
        name=request.form['name']
    )
    return redirect(url_for('choose_enemy'))


@app.route('/choose-enemy', methods=['GET', 'POST'])
def choose_enemy():
    if request.method == 'GET':
        return render_template(
            'hero_choosing.html',
            result= {
                "header": "Выберите противника",
                "classes": character_classes,
                "weapons": RESULT.get_weapon_names,
                "armors": RESULT.get_armor_names,
            }
        )
    heroes['enemy'] = Enemy(
        unit_class=character_classes[request.form['unit_class']],
        weapon=load_equipment().get_weapon(request.form['weapon']),
        armor=load_equipment().get_armor(request.form['armor']),
        name=request.form['name']
    )
    return redirect(url_for('start_fight'))


@app.route('/fight')
def start_fight():
    if 'player' in heroes and 'enemy' in heroes:
        game.run(**heroes)
        return render_template('fight.html', heroes=heroes, result='Начало боя')
    return redirect(url_for('index'))


@app.route('/fight/hit')
@game_processing
def hit():
    return render_template('fight.html', heroes=heroes, result=game.player_hit())


@app.route('/fight/use-skill')
@game_processing
def user_skill():
    return render_template('fight.html', heroes=heroes, result=game.player_use_skill())


@app.route('/fight/pass-turn')
@game_processing
def pass_turn():
    return render_template('fight.html', heroes=heroes, result=game.next_turn())


@app.route('/fight/end-fight')
def end_fight():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
