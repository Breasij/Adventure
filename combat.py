import random
from enemy import EnemyData


def combat_sequence(player, enemy): 
    print(f"A wild {enemy.name} appears! ({enemy.hp} HP) - {enemy.description}")

    while player.hp > 0 and enemy.hp > 0:
        action = input("Do you [A]ttack or [R]un? ").lower()
        
        if action == 'a':
            attack_roll = random.randint(1, 20) + player.attack_power
            print(f"You roll a {attack_roll} to attack (Enemy AC: {enemy.ac})")

            if attack_roll >= enemy.ac:
                damage = player.attack()
                enemy.hp -= damage
                print(f"You dealt {damage} damage to the {enemy.name}! (Enemy HP: {enemy.hp})")
            else:
                print("Your attack missed!")

        elif action == 'r':
            if random.random() > 0.5:
                print("You successfully escaped!")
                return
            else:
                print("Escape failed!")

        if enemy.hp > 0:
            enemy_damage = enemy.attack()
            player.hp -= enemy_damage
            print(f"The {enemy.name} attacks you for {enemy_damage} damage! (Your HP: {player.hp})")

    if player.hp <= 0:
        print("You were defeated...")
    else:
        print(f"You defeated the {enemy.name}!")
        # Handling drops after combat:
        if enemy.drops:
            print("You search the enemy and find:")
            for item_name, drop_info in enemy.drops.items():
                if random.random() <= drop_info['chance']:
                    quantity = random.randint(drop_info['quantity'][0], drop_info['quantity'][1])
                    player.inventory[item_name] = player.inventory.get(item_name, 0) + quantity
                    print(f"- {quantity} x {item_name}")
                else:
                    print(f"- No {item_name} this time.")