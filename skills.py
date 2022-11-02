from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """Базовый класс умения"""
    user: Any = None
    target: Any = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self) -> bool:
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use"""
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name: str = "Свирепый пинок"
    stamina: float = 6
    damage: float = 12

    def skill_effect(self) -> str:
        """Логика использования скилла"""
        self.target.get_damage(self.damage)
        self.user.stamina -= self.stamina
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."


class HardShot(Skill):
    name: str = "Мощный укол"
    stamina: float = 5
    damage: float = 15

    def skill_effect(self) -> str:
        """Логика использования скилла"""
        self.target.get_damage(self.damage)
        self.user.stamina -= self.stamina
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."
