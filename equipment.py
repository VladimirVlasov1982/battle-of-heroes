from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: int
    stamina_per_turn: int


@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: int


    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    """Содержит 2 списка - с оружием и с броней"""
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self) -> None:
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        """Возвращает объект оружия по имени"""
        for weapon in self.equipment.weapons:
            if weapon_name == weapon.name:
                return weapon
        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        """Возвращает объект брони по имени"""
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> list:
        """Возвращаем список с оружием"""
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        """Возвращаем список с броней"""
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """Этот метод загружает json в переменную EquipmentData"""
        with open("./data/equipment.json", encoding="utf-8") as file:
            data = json.load(file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
