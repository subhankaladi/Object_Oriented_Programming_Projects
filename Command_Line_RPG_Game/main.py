import random
from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass

# Abstraction: Enum simplifies character class handling
class CharacterClass(Enum):
    WARRIOR = auto()
    MAGE = auto()
    ROGUE = auto()

@dataclass
class Weapon:
    name: str
    damage: int
    durability: int

# Abstraction + Inheritance: Base abstract class for all character types
class Character(ABC):  # Abstraction
    def __init__(self, name: str, character_class: CharacterClass):
        # Encapsulation: All character-related properties are bundled inside the class
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.health = 100
        self.weapon = None
        self.inventory = []
        self._initialize_class()  # Polymorphism: method is redefined by subclasses

    @abstractmethod
    def _initialize_class(self):
        pass

    def attack(self, target):
        if not self.weapon:
            print(f"{self.name} has no weapon to attack with!")
            return

        damage = random.randint(self.weapon.damage // 2, self.weapon.damage)
        target.health -= damage
        self.weapon.durability -= 1

        print(f"{self.name} attacks {target.name} with {self.weapon.name} for {damage} damage!")

        if self.weapon.durability <= 0:
            print(f"{self.name}'s {self.weapon.name} broke!")
            self.weapon = None

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        print(f"{self.name} equipped {weapon.name}!")

    def level_up(self):
        self.level += 1
        self.health += 20
        print(f"{self.name} leveled up to level {self.level}!")

    def is_alive(self):
        return self.health > 0

# Inheritance: Warrior inherits from Character
# Polymorphism: Overrides _initialize_class to customize Warrior
class Warrior(Character):  # Inheritance
    def _initialize_class(self):  # Polymorphism
        self.health = 120
        self.equip_weapon(Weapon("Rusty Sword", 15, 10))

# Inheritance + Polymorphism: Mage inherits and modifies attack behavior
class Mage(Character):  # Inheritance
    def _initialize_class(self):  # Polymorphism
        self.health = 80
        self.equip_weapon(Weapon("Wooden Staff", 20, 5))

    def attack(self, target):  # Polymorphism
        super().attack(target)
        if random.random() < 0.3:
            magic_damage = random.randint(5, 15)
            target.health -= magic_damage
            print(f"Magic burst hits {target.name} for additional {magic_damage} damage!")

# Inheritance + Polymorphism: Rogue inherits and defines its unique attack
class Rogue(Character):  # Inheritance
    def _initialize_class(self):  # Polymorphism
        self.health = 90
        self.equip_weapon(Weapon("Dagger", 12, 15))

    def attack(self, target):  # Polymorphism
        super().attack(target)
        if random.random() < 0.4:
            crit_damage = random.randint(10, 20)
            target.health -= crit_damage
            print(f"Critical strike! {target.name} takes extra {crit_damage} damage!")

# Encapsulation: Game logic wrapped in a class to manage state and flow
class Game:
    def __init__(self):
        self.player = None
        self.enemies = []
        self.current_floor = 1
        self.game_over = False

    def start_game(self):
        print("Welcome to Python RPG!")
        name = input("Enter your character name: ")
        print("Choose your class:")
        for i, char_class in enumerate(CharacterClass, 1):
            print(f"{i}. {char_class.name}")
        
        class_choice = int(input("Select class (1-3): ")) - 1
        char_class = list(CharacterClass)[class_choice]

        # Polymorphism: Using same type (Character) to refer to different class instances
        if char_class == CharacterClass.WARRIOR:
            self.player = Warrior(name, char_class)
        elif char_class == CharacterClass.MAGE:
            self.player = Mage(name, char_class)
        else:
            self.player = Rogue(name, char_class)

        self._generate_enemies()
        self._game_loop()

    def _generate_enemies(self):
        enemy_classes = ["Goblin", "Orc", "Skeleton", "Zombie"]
        for i in range(3):
            enemy_type = random.choice(enemy_classes)
            enemy_class = random.choice(list(CharacterClass))

            if enemy_class == CharacterClass.WARRIOR:
                enemy = Warrior(f"{enemy_type} Warrior", enemy_class)
            elif enemy_class == CharacterClass.MAGE:
                enemy = Mage(f"{enemy_type} Mage", enemy_class)
            else:
                enemy = Rogue(f"{enemy_type} Rogue", enemy_class)

            enemy.level = self.current_floor
            enemy.health += (self.current_floor - 1) * 10
            self.enemies.append(enemy)

    def _game_loop(self):
        while not self.game_over and self.player.is_alive():
            print(f"\n=== Floor {self.current_floor} ===")
            print(f"{self.player.name} (Level {self.player.level}) - HP: {self.player.health}")

            if not self.enemies:
                print("No enemies remaining! Moving to next floor...")
                self.current_floor += 1
                self._generate_enemies()
                self.player.level_up()
                continue

            print("\nEnemies:")
            for i, enemy in enumerate(self.enemies, 1):
                print(f"{i}. {enemy.name} (Level {enemy.level}) - HP: {enemy.health}")

            print("\nActions:")
            print("1. Attack")
            print("2. Check Inventory")
            print("3. Flee (50% chance)")

            choice = input("Choose action: ")

            if choice == "1":
                enemy_choice = int(input("Select enemy to attack (1-3): ")) - 1
                if 0 <= enemy_choice < len(self.enemies):
                    self.player.attack(self.enemies[enemy_choice])

                    if not self.enemies[enemy_choice].is_alive():
                        print(f"{self.enemies[enemy_choice].name} was defeated!")
                        self.enemies.pop(enemy_choice)

                    for enemy in self.enemies:
                        enemy.attack(self.player)
                        if not self.player.is_alive():
                            print("Game Over! You were defeated.")
                            self.game_over = True
                            break
                else:
                    print("Invalid enemy selection!")

            elif choice == "2":
                print("\nInventory:")
                if self.player.weapon:
                    print(f"Weapon: {self.player.weapon.name} (Dmg: {self.player.weapon.damage}, Dur: {self.player.weapon.durability})")
                else:
                    print("No weapon equipped!")

            elif choice == "3":
                if random.random() < 0.5:
                    print("You successfully fled from battle!")
                    self.enemies.clear()
                else:
                    print("Failed to flee! Enemies attack!")
                    for enemy in self.enemies:
                        enemy.attack(self.player)
                        if not self.player.is_alive():
                            print("Game Over! You were defeated.")
                            self.game_over = True
                            break

            else:
                print("Invalid choice!")

if __name__ == "__main__":
    game = Game()
    game.start_game()
