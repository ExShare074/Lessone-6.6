#Создаем простую текстовую боевую игру, где игрок и компьютер управляют героями с различными характеристиками.

# Класс Hero:
# Атрибуты:
# Имя (name)
# Здоровье (health), начальное значение 100
# Сила удара (attack_power), начальное значение 20

# Методы:
# attack(other): атакует другого героя (other), отнимая здоровье в размере своей силы удара
# is_alive(): возвращает True, если здоровье героя больше 0, иначе False

# Класс Game:
# Атрибуты:
# Игрок (player), экземпляр класса Hero
# Компьютер (computer), экземпляр класса Hero

# Методы:
# start(): начинает игру, чередует ходы игрока и компьютера, пока один из героев не умрет.
# Выводит информацию о каждом ходе (кто атаковал и сколько здоровья осталось у противника) и объявляет победителя.

import random


class Hero:
    def __init__(self, name, health=100, attack_power=20):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other):
        damage = random.randint(0, self.attack_power)
        other.health -= damage
        return damage

    def is_alive(self):
        return self.health > 0


class Game:
    def __init__(self, player_name, computer_name="Computer"):
        self.player = Hero(player_name)
        self.computer = Hero(computer_name)

    def start(self):
        print("Игра началась!")
        print(f"{self.player.name} против {self.computer.name}")

        while self.player.is_alive() and self.computer.is_alive():
            # Ход игрока
            damage = self.player.attack(self.computer)
            print(f"{self.player.name} атаковал {self.computer.name} и нанес {damage} урона.")
            print(f"Здоровье {self.computer.name}: {self.computer.health}")

            if not self.computer.is_alive():
                print(f"{self.computer.name} погиб. {self.player.name} победил!")
                break

            # Ход компьютера
            damage = self.computer.attack(self.player)
            print(f"{self.computer.name} атаковал {self.player.name} и нанес {damage} урона.")
            print(f"Здоровье {self.player.name}: {self.player.health}")

            if not self.player.is_alive():
                print(f"{self.player.name} погиб. {self.computer.name} победил!")
                break


if __name__ == "__main__":
    player_name = input("Введите имя вашего героя: ")
    game = Game(player_name)
    game.start()




