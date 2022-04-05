from typing import Optional

from game.hero import Hero, Enemy


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):

    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_processing = False
        self.game_results = ''

    def run(self, player: Hero, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.game_processing = True

    def _check_hp(self) -> Optional[str]:
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            return self._end_game(results='Никто не выжил')
        if self.player.hp <= 0:
            return self._end_game(results='Противник сделал невозможное, как ты мог проиграть?')
        if self.enemy.hp <= 0:
            return self._end_game(results='Игрок вышел победителем в этой схватке')
        return None

    def _end_game(self, results: str):
        self.game_processing = False
        self.game_results = results
        return results

    def next_turn(self) -> str:
        if results := self._check_hp():
            return results
        if not self.game_processing:
            return self.game_results

        dealt_damage: Optional[float] = self.enemy.hit(self.player)
        if dealt_damage is not None:
            self.player.take_hit(dealt_damage)
            results = f'Противник нанес тебе {dealt_damage} урона '
        else:
            results = 'У противника не хватает выносливости на удар '
        self._stamina_regenerate()
        return results

    def _stamina_regenerate(self):
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

    def player_hit(self) -> str:
        dealt_damage: Optional[float] = self.player.hit(self.enemy)
        if dealt_damage is not None:
            self.enemy.take_hit(dealt_damage)
            return f'Ты нанёс противнику {dealt_damage} урона {self.next_turn()} '
        return f'Не хватило выносливости на удар {self.next_turn()} '

    def player_use_skill(self) -> str:
        dealt_damage: Optional[float] = self.player.use_skill()
        if dealt_damage is not None:
            self.enemy.take_hit(dealt_damage)
            return f'Ты нанёс противнику {dealt_damage} урона {self.next_turn()} '
        return f'Не хватило выносливости на использование способности {self.next_turn()} '
