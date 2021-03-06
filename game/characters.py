from abc import ABC
from typing import Dict, Type

from game.skills import Skill, ferocious_kick, powerful_thrust


class Character(ABC):
    name: str = NotImplemented
    max_health: float = NotImplemented
    max_stamina: float = NotImplemented
    stamina: float = NotImplemented
    attack: float = NotImplemented
    armor: float = NotImplemented
    skill: Skill = NotImplemented


class Warrior(Character):
    name = 'Воин'
    max_health: float = 60.0
    max_stamina: float = 30.0
    stamina: float = 0.8
    attack: float = 0.9
    armor: float = 1.2
    skill: Skill = ferocious_kick


class Thief(Character):
    name = 'Вор'
    max_health: float = 50.0
    max_stamina: float = 25.0
    stamina: float = 1.2
    attack: float = 1.5
    armor: float = 1.0
    skill: Skill = powerful_thrust


character_classes: Dict[str, Type[Character]] = {
    Warrior.name: Warrior,
    Thief.name: Thief,
}
