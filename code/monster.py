class Monster:
    def __init__(self, override_attack: callable = None):
        self.attack_override = override_attack

    health: int = 90
    energy: int = 40

    def attack(self, amount):
        print('The monster has attacked!')
        print(f'{amount} damage dealt')
        self.energy -= 21
        print(f'Remaining energy: {self.energy}')

    def move(self, speed):
        print('The monster is moving')
        print(f'The speed is {speed}')

    def take_damage(self, amount):
        print('The monster has taken damage!')
        print(f'{amount} damage taken')
        self.health -= amount
        print(self.health)


class Shark(Monster):
    def __init__(self, initial_speed: int, override_attack: callable = None):
        super().__init__(override_attack)
        self.speed = initial_speed


class Attacks:
    def bite(self):
        print('Bite!')

    def strike(self):
        print('Strike!')

    def slash(self):
        print('Slash!')

    def kick(self):
        print('Kick!')


class Hero:
    def __init__(self, damage: int, monster: Monster):
        self.damage = damage
        self.monster = monster

    def attack(self):
        print('The hero has attacked!')
        self.monster.take_damage(self.damage)


attacks: Attacks = Attacks()
# monster: Monster = Monster(my_attack=attacks.bite)
# monster.attack()
# hero: Hero = Hero(damage=10, monster=monster)

shark: Shark = Shark(initial_speed=50)
shark.attack(30)
# hero.attack()
