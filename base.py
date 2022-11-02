from typing import Optional, Any
from unit import BaseUnit


class BaseSingleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs) -> dict:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND: int = 1
    player: Any = None
    enemy: Any = None
    game_is_running: bool = False
    battle_result: Optional[str] = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        """НАЧАЛО ИГРЫ. Присваиваем экземпляру класса аттрибуты "игрок" и "противник",
         а также выставляем True для свойства "началась ли игра" """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """Проверка здоровья игрока и врага"""
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        elif self.player.hp <= 0:
            self.battle_result = "Игрок проиграл битву"
        else:
            self.battle_result = "Игрок выиграл битву"

        return self._end_game()

    def _stamina_regeneration(self) -> None:
        """Регенерация здоровья и стамины для игрока и врага за ход"""
        units: list = [self.player, self.enemy]
        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self) -> Any:
        """СЛЕДУЮЩИЙ ХОД.
        Срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        """
        result: Optional[str] = self._check_players_hp()
        if result is not None:
            return result

        if self.game_is_running:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def _end_game(self) -> Optional[str]:
        """КНОПКА ЗАВЕРШЕНИЕ ИГРЫ"""
        self._instances: dict = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        """КНОПКА УДАР ИГРОКА"""
        player_result: str = self.player.hit(self.enemy)
        enemy_result: str = self.next_turn()
        return f"{player_result}<br>{enemy_result}"

    def player_use_skill(self) -> str:
        """КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ"""
        player_result: str = self.player.use_skill(self.enemy)
        enemy_result: str = self.next_turn()
        return f"{player_result}<br>{enemy_result}"
