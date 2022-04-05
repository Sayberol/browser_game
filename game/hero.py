from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import Type, Optional

from game.characters import Character
from game.equipment import Weapon, Armor

BASE_STAMINA_PER_ROUND = 0.4


class Hero(ABC):
    def __init__(self, unit_class: Type[Character], weapon: Weapon, armor: Armor, name: str):
        self.unit_class = unit_class
        self.weapon = weapon
        self.armor = armor
        self.stamina_points = self.unit_class.max_stamina
        self.health_points = self.unit_class.max_health
        self.skill_used: bool = False
        self.name = name

    @property
    def hp(self):
        return round(self.health_points, 1)

    @hp.setter
    def hp(self, value):
        self.health_points = value

    @property
    def stamina(self):
        return round(self.health_points, 1)

    @stamina.setter
    def stamina(self, value):
        self.stamina_points = value

    @property
    def _target_armor(self) -> float:
        if self.stamina - self.armor.stamina_per_turn >= 0:
            return self.armor.defence * self.unit_class.armor
        return 0

    def _hit(self, target: Hero) -> Optional[float]:
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None

        hero_damage = self.weapon.damage * self.unit_class.attack
        dealt_damage = hero_damage - target._target_armor
        if dealt_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(dealt_damage, 1)

    def take_hit(self, damage: float):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def regenerate_stamina(self):
        delta_stamina = BASE_STAMINA_PER_ROUND * self.unit_class.stamina
        if self.stamina + delta_stamina <= self.unit_class.max_stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.unit_class.max_stamina

    def use_skill(self) -> Optional[float]:
        if not self.skill_used and self.stamina - self.unit_class.skill.stamina:
            self.skill_used = True
            return round(self.unit_class.skill.damage, 1)
        return None

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        ...


class Enemy(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        if random.randint(0, 100) < 10 and self.stamina >= self.unit_class.skill.stamina and not self.skill_used:
            self.use_skill()
        return self._hit(target)


class Player(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        return self._hit(target)
