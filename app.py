from flask import Flask, render_template, request, redirect, url_for
from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes: dict = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    """Главное меню"""
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    """Выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы"""
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit():
    """Кнопка нанесения удара"""
    if arena.game_is_running:
        result: str = arena.player_hit()
    else:
        result: str = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """Кнопка использования скилла"""
    if arena.game_is_running:
        result: str = arena.player_use_skill()
    else:
        result: str = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """Кнопка пропус хода"""
    if arena.game_is_running:
        result: str = arena.next_turn()
    else:
        result: str = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """Кнопка завершить игру - переход в главное меню"""
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """Кнопка выбор героя. 2 метода GET и POST. На GET отрисовываем форму.
    На POST отправляем форму и делаем редирект на эндпоинт choose enemy"""
    if request.method == "GET":
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            "header": "Выберите героя",
            "classes": classes,
            "weapons": weapons,
            "armors": armors,
        }
        return render_template("hero_choosing.html", result=result)
    elif request.method == "POST":
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']
        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        player.equip_armor(equipment.get_armor(armor_name))
        player.equip_weapon(equipment.get_weapon(weapon_name))
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """Кнопка выбор соперника.
    2 метода GET и POST. На GET отрисовываем форму.
    На POST отправляем форму и делаем редирект на начало битвы"""
    if request.method == "GET":
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            "header": "Выберите противника",
            "classes": classes,
            "weapons": weapons,
            "armors": armors,
        }
        return render_template("hero_choosing.html", result=result)
    elif request.method == "POST":
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']
        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        enemy.equip_armor(equipment.get_armor(armor_name))
        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
