import random

# =========================
# TITLE SCREEN
# =========================
def title_screen():
    print("======================================")
    print("  ███████╗     ██████╗     ██    ██ ")
    print("  ██          ██    ██     ██    ██ ")
    print("  ███████╗    ██    ██     ██    ██ ")
    print("       ██     ██    ██     ██    ██ ")
    print("  ███████╗     ██████╗      ██████  ")
    print()
    print("          SHADOWS OF VALOR")
    print("======================================")
    input("Press Enter to begin...")

# =========================
# INTRO
# =========================
def show_intro():
    print("\nDarkness spreads across the land.")
    print("Legends tell of a great hero who can defeat the Shadow King.")
    print("Will you complete the great journey?\n")

# =========================
# HUD
# =========================
def draw_bar(current, maximum, label):
    if current < 0:
        current = 0
    bar_length = 20
    filled = int(bar_length * current // maximum)
    bar = "█" * filled + "-" * (bar_length - filled)
    print(f"{label}: |{bar}| {current}/{maximum}")

def mini_hud(player):
    print("\n==============================")
    print(f"{player.name} | {player.player_class.upper()}")
    print(f"HP   : |{'█'*int(20*player.health/200)+'-'*(20-int(20*player.health/200))}| {player.health}/200")
    print(f"Mana : |{'█'*int(20*player.mana/100)+'-'*(20-int(20*player.mana/100))}| {player.mana}/100")
    print(f"Attack: {player.base_attack}")
    print(f"Potions → H:{player.inventory['health potion']} | M:{player.inventory['mana potion']}")
    if player.spells:
        print("Spells:", ", ".join([s.title() for s in player.spells]))
    print("==============================")

# =========================
# PLAYER
# =========================
class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.health = 150
        self.mana = 60
        self.base_attack = 20
        self.spells = []
        self.revive_available = True
        self.weapon = None
        self.inventory = {"health potion": 0, "mana potion": 0}

        if player_class == "warrior":
            self.base_attack = 30
        elif player_class == "mage":
            self.mana = 150
        elif player_class == "cleric":
            self.mana = 200
        elif player_class == "ogre":
            self.health = 160

    def attack(self, enemy):
        damage = self.base_attack
        if self.player_class == "warrior" and self.weapon and self.weapon[0].lower() in ["sword","hammer","mace","axe"]:
            damage *= 1.15

        if random.random() < 0.10:
            damage *= 2
            print("💥 CRITICAL HIT!")

        damage = int(damage)
        enemy.health -= damage
        print(f"You deal {damage} damage to {enemy.name}!")

        if enemy.health <= 0 and self.player_class == "ogre":
            self.base_attack += 10
            print("🔥 Ogre rage increases your attack permanently!")

# =========================
# ENEMY + BOSS
# =========================
class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

class Boss(Enemy):
    def __init__(self):
        super().__init__("Shadow King", 300, 18)
        self.phase_two = False

    def special_attack(self, player):
        damage = random.randint(16, 32)
        player.health -= damage
        print(f"🌑 Dark Nova hits you for {damage} damage!")

# =========================
# SPELLS
# =========================
SPELLS_INFO = {
    "fireball": {"damage": 40, "mana": 15, "desc": "Deals 40 damage"},
    "ice bolt": {"damage": 35, "mana": 15, "desc": "Deals 35 damage"},
    "lightning wave": {"damage": 20, "mana": 15, "desc": "Hits all enemies for 20 damage"},
    "curse": {"damage": 15, "mana": 20, "desc": "Deals 15 damage + 5% life steal"},
    "healing aura": {"heal": 30, "mana": 20, "desc": "Restores 30 HP"},
    "guiding light": {"buff": 10, "mana": 15, "desc": "Increases attack by 10"},
    "sacred flame": {"damage": 40, "mana": 25, "desc": "Deals 40 damage"},
    "revive": {"mana": 50, "desc": "Revive yourself if defeated"}
}

def cast_spell(player, enemies, spell):
    spell = spell.lower()
    info = SPELLS_INFO.get(spell, {})
    cost = info.get("mana", 0)
    if player.mana < cost:
        print("Not enough mana!")
        return

    player.mana -= cost

    if "damage" in info:
        if spell == "lightning wave":
            for e in enemies:
                e.health -= info["damage"]
            print(f"⚡ Lightning Wave hits all enemies for {info['damage']} damage each!")
        elif spell == "curse":
            enemies[0].health -= info["damage"]
            steal = int(enemies[0].health * 0.05)
            player.health += steal
            print(f"🩸 Curse deals {info['damage']} damage and steals {steal} HP!")
        else:
            enemies[0].health -= info["damage"]
            print(f"{spell.capitalize()} deals {info['damage']} damage!")
    elif "heal" in info:
        player.health += info["heal"]
        print(f"💚 {spell.capitalize()} restores {info['heal']} HP!")
    elif "buff" in info:
        player.base_attack += info["buff"]
        print(f"🌟 {spell.capitalize()} increases your attack by {info['buff']}!")
    elif spell == "revive":
        if player.health <= 0 and player.revive_available:
            player.health = 50
            player.revive_available = False
            print("✨ Revive spell restores you to 50 HP!")
        else:
            print("Revive cannot be used now!")

# =========================
# POTIONS
# =========================
def use_potions(player):
    while True:
        available = [p for p, qty in player.inventory.items() if qty > 0]
        if not available:
            return
        choice = input("Use potion? (health/mana/skip): ").lower()
        if choice == "skip":
            break
        elif choice == "health" and player.inventory["health potion"] > 0:
            player.health = min(200, player.health + 50)
            player.inventory["health potion"] -= 1
            print("💖 +50 HP")
        elif choice == "mana" and player.inventory["mana potion"] > 0:
            player.mana = min(100, player.mana + 50)
            player.inventory["mana potion"] -= 1
            print("🔵 +50 Mana")
        else:
            print("⚠ Invalid or no potions of that type.")

# =========================
# CHESTS
# =========================
def open_chest(player):
    mage_spells = ["fireball","ice bolt","lightning wave","curse"]
    cleric_spells = ["healing aura","revive","guiding light","sacred flame"]
    if player.player_class == "mage":
        spell = random.choice(mage_spells)
    elif player.player_class == "cleric":
        spell = random.choice(cleric_spells)
    else:
        spell = random.choice(["fireball","healing aura","curse"])
    if spell not in player.spells:
        player.spells.append(spell)
        print(f"📦 You found a new spell: {spell}!")
    potion = random.choice(["health potion","mana potion"])
    player.inventory[potion] += 1
    print(f"🍾 You found a {potion.replace('_',' ')}!")

# =========================
# BATTLE
# =========================
def battle(player, enemies):
    print("\n⚔ BATTLE BEGINS!")
    turn = 1
    while player.health > 0 and any(e.health > 0 for e in enemies):
        print(f"\n--- TURN {turn} ---")
        mini_hud(player)
        for i, e in enumerate(enemies):
            if e.health > 0:
                draw_bar(e.health, 100, f"{i+1}. {e.name}")
        use_potions(player)
        choice = input("Action (1=Attack, 2=Spell): ").lower()
        if choice in ["1","attack"]:
            target = int(input("Target #: "))-1
            if 0 <= target < len(enemies) and enemies[target].health > 0:
                player.attack(enemies[target])
        elif choice in ["2","spell"] and player.spells:
            for i,s in enumerate(player.spells):
                info = SPELLS_INFO.get(s,{})
                print(f"{i+1}. {s.title()} - {info.get('desc','')} ({info.get('mana',0)} Mana)")
            idx = int(input("Spell #: "))-1
            if 0 <= idx < len(player.spells):
                cast_spell(player, enemies, player.spells[idx])
        for e in enemies:
            if e.health > 0:
                player.health -= e.attack
                print(f"{e.name} hits for {e.attack}!")
        if player.health <= 0 and player.player_class=="cleric" and player.revive_available:
            player.health = 50
            player.revive_available=False
            print("✨ Divine Revive activates!")
        turn+=1
    if player.health > 0:
        print("🏆 Victory!")
        open_chest(player)
    else:
        print("💀 You were defeated...")

# =========================
# PATHS
# =========================
def forest_path(player):
    print("\n🌲 Entering the Dark Forest...")
    enemy_sets=[[Enemy("Goblin",40,8)],[Enemy("Wolf",35,10)],[Enemy("Evil Gnome",30,12)]]
    multi_battle(player, enemy_sets)

def cave_path(player):
    print("\n🦴 Entering the Cursed Cave...")
    enemy_sets=[[Enemy("Skeleton",40,10)],[Enemy("Zombie",40,8)],[Enemy("Slime Monster",60,12)]]
    multi_battle(player, enemy_sets)

def village_path(player):
    print("\n🏚 Entering the Ruined Village...")
    enemy_sets=[[Enemy("Vampire",25,5),Enemy("Vampire",25,5),Enemy("Familiar",15,3)],
                [Enemy("Witch",35,7),Enemy("Slightly smaller Witch",25,5)]]
    multi_battle(player, enemy_sets)
    print("\n🎁 You find extra treasure hidden among the ruins!")
    for _ in range(2):
        open_chest(player)

def multi_battle(player, enemy_sets):
    for enemies in enemy_sets:
        battle(player, enemies)
        if player.health <= 0:
            break

def choose_path():
    print("\nChoose your path:\n1. Dark Forest\n2. Cursed Cave\n3. Ruined Village")
    while True:
        choice = input("Enter 1-3: ")
        if choice in ["1","2","3"]:
            return choice
        print("Invalid choice.")

def resolve_path(choice, player):
    if choice=="1":
        forest_path(player)
    elif choice=="2":
        cave_path(player)
    elif choice=="3":
        village_path(player)
    if player.health>0:
        final_boss_battle(player)

# =========================
# FINAL BOSS
# =========================
def final_boss_battle(player):
    boss = Boss()
    print("\nThe sky darkens...\nThe ground trembles.\n👑 THE SHADOW KING EMERGES 👑")
    print("░░░░░░░░░░░░ ▄▐")
    print("░░░░░░▄▄▄░░▄██▄")
    print("░░░░ ▐ ͡° ͜ʖ ͡° '▌░░░▀█▄")
    print("░░░░░▐███▌░░░░░░▀█▄")
    print("░░░░░░▀▄▀░░░▄▄▄▄▄▀▀")
    print("░░░░▄▄▄██▀▀▀▀")
    print("░░░█▀▄▄▄█░▀▀")
    print("░░░▌░▄▄▄▐▌▀▀▀")
    print("▄░▐░░░▄▄░█░▀▀ U HAVE BEEN BANGED BY THE SHADOW KING!")
    print("▀█▌░░░▄░▀█▀░▀")
    print("░░░░░░░▄▄▐▌▄▄")
    print("░░░░░░░▀███▀███▀██▀██▀██▀░▄")
    print("░░░░░░▐▌▀▄▀▄▀▐▄")
    print("░░░░░░▐▀░░░░░░▐▌")
    print("░░░░░░█░░░░░░░░█")
    print("░░░░░▐▌░░░░░░░░░█DEFEAT THE SHADOW KING OR NOT I DONT REALLY CARE")
    print("░░░░░█░░░░░░░░░░▐")
    turn = 1
    taunts = ["You are nothing before darkness!","You think you can defeat me?","Kneel before your king!",
              "Darkness wil envelop the WORLD!","Your foolishness will be your downfall"]
    while player.health>0 and boss.health>0:
        print(f"\n=== FINAL BOSS TURN {turn} ===")
        mini_hud(player)
        draw_bar(boss.health,300,"Shadow King")
        use_potions(player)
        choice = input("Action (1=Attack,2=Spell): ").lower()
        if choice in ["1","attack"]:
            player.attack(boss)
        elif choice in ["2","spell"] and player.spells:
            for i,s in enumerate(player.spells):
                info = SPELLS_INFO.get(s,{})
                print(f"{i+1}. {s.title()} - {info.get('desc','')} ({info.get('mana',0)} Mana)")
            idx = int(input("Spell #: "))-1
            if 0 <= idx < len(player.spells):
                cast_spell(player,[boss],player.spells[idx])
        if boss.health <= 100 and not boss.phase_two:
            boss.phase_two=True
            boss.attack += 7
            print("🔥 The Shadow King enters PHASE TWO!")
        if boss.health>0:
            if random.random()<0.3:
                print(f"\nShadow King: '{random.choice(taunts)}'")
            if boss.phase_two and random.random()<0.4:
                boss.special_attack(player)
            else:
                player.health -= boss.attack
                print(f"Shadow King strikes for {boss.attack}!")
        turn+=1
    if player.health>0:
        print("\n🏆 YOU HAVE DEFEATED THE SHADOW KING!")
        print("Shadow King:")
        print("ughhhh *coughs blood*")
        print("Foolish mortal... you cannot kill that which is eternal")
        print("There will always be darkness in the world")
        print("                          #####%%%%#*                          #%%%%%%######                        ")
        print("                        #####%%%%%#**                          %%%%%%%%%#####                        ")
        print("                       ##*##%%%%%##*                            #%%%%%%%%####*                       ")
        print("                      #####%%%%%%##           ---:      :::      %%%%%%%%%###**                      ")
        print("                     #####%%%%%###           =-.:--   --..:-       %%%%%%%%###*                      ")
        print("                     ####%%%%%#*=          ++=---::  =--::::       #%%%%%%%%##**                    ")
        print("                    ##*#%%%%%%#*-          +++++    +====-::       #%%%%%%%%%#**                    ")
        print("                    *##%%%%%%%%#          *+=+#    ++==** ::       #%%%%%%%%%#**==                  ")
        print("                  ##*##%%%%%%%##*         ++++    ++=**            ###%%%%%%%%#*++                  ")
        print("                 #**##%%%%%%%%##          +***   *+++*#            %%%%%%%%%%%%#***                  ")
        print("                %***#%%%%%%%%%#%#        ***######++***            ###%%%%%%%%%%#**##                ")
        print("              %##**#%%%%%%%%%%###        **#%%####**##             %%%%%%%%%%%%%%##**##              ")
        print("             ###**#%%%%%%%%%%%%%#*  *     #####**###%%****   *#  #%%%%%%%%%%%%%%%%#***##            ")
        print("            ##***#%%%%%%%%%%%%%%%%%#####**###*+=++*#%#*##  ######%%%%%%%%%%%%%%%%%%%#**##           ")
        print("          ##****#%%%%%%%%%%%%%%%%%%%%####*###*====*####%% #%%###%%%%%%%%%%%%%%%%%%%%%#*****         ")
        print("         ##****#%%%%%%%%%%%%%%%%%%%%%%%######*++++*###* ##%###%%%%%%%%%%%%%%%%%%%%%%%%#****#        ")
        print("       ###****##%%%%%%%%%%%%%%%%%%%%%%%##%%%#******##%%%%#####%%%%%%%%%%%%%%%%%%%%%%%%##**###       ")
        print("        #****##%#%%%%%%%%%%%%%%%%%%%%%%###%%#******#%%%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%##***##       ")
        print("       ******##%####%%%%%%%%%%%%%%%%%%%%%#%%##****##%%%%%%%##%%%%%%%%%%%%%%%%%%%%#######******      ")
        print("     ###*****#######%%%%%%%%%%%%%%%%%%######%%####%%%%%####****####%%%%%%%%%%%%#########*****+++    ")
        print("    #***#****########%%%%%%%%%#%%%%%##***######%####%#####***######**%%%%%%%%%##########*****+++    ")
        print("    #*###***####### ##%%%%%%%  %%%####***###################***######**%%%%####  ######**++****+=   ")
        print("    ##*##***####### %%%%%%%  %%%%#####*****+******##*****#%%#***#######%%%##### ####****+++*****+   ")
        print("   **** #++*#######*#%%%#%% #########*###***++++++*++++*###%%%#########+ %#####****#***++====+++++  ")
        print("   *** **++*#######*###     ** #######%%#****++*****+*****##%%%%#####%#**   #*********+++====  +++  ")
        print("  **# *+++***######            %#####%%%%###**######****###%%%%%%%###%##*     ********+======+   =  ")
        print("      +==+*********          %%%####%##%%%%%###%##%%####%%%%%%%%%%%#####**       +**+++=----==      ")
        print("      ===+++++++++*          %%######*+*%%%%%%%%%%%%%%%%%%%%%%%%%%%#######*      +++++*+-----=      ")
        print("      ===+++++++++          ##%#**##*+    %%%%%%%%%%%%%%%%%%%%%%%%#%#*##%#**      ++++++=----==     ")
        print("    ==-========++           %##**####      %#%%%%%%%%%%%%%%%%%%%#* %%######+=      +++++=-------    ")
        print("    ---========            #%##**#*-          #%%%%%%%%%%%%%%%%#+=  %%#####**       -=++==--:---    ")
        print("   --:-===-----           %%%####**            ##%%%%%%%%%%%%%#**     %%######%      ====-----::-   ")
        print("  -:-------::::         %%%%#%%%#*+             ##%%%%%%%%%%###**     %%####%%%#     -------::::::  ")
        print(" -:::-----:::::        %%#####%##+             *#################     %%#####%##    =-:----:::::.:: ")
        print(" ::::--:::::::         %%#######*               ###############*       %%####%%##    ------:::::.:: ")
        print(" ::::::::::::         #%%#######                ##########*####         %##*###%%%     ---::::::.:: ")
        print(":::::::::::           ########                 =*******#*******          %###*##%%      --::::::::: ")
        print("::::::::::::         %%####%%#                ++***********+++*           ######%%      :::-::::::::")
        print("::::::::::::         %#####%%                 ++++++++++++++=++            #####%##     ::::::::::::")
        print(":::::::::::          #####%                   =-=====+===+====+             %%#####      ::::::::.::")
        print(":::...::::          %######                  ::-----======-----              ######      :::::.:::::")
        print(" :::...:            ######                   ::::-:-----------                #####*        ::...:: ")
        print(" :::..::          %%####**                   ::::::::----::::-                 %%##**       ::..::: ")
        print("::::...:          ####****                 :::::::::::--:::::                  %%####       ::..::::")
        print("::...::          #####**##                 ::..::::::::::::::                  ######%      ::::::::")
        print("::...::          #####**##                 ::..::::::::::::::                  ######%#         ::  ")
        print(" :::             #####+*##                 ::..::::::::::::::                  ########%            ")
        print("                 ######*#                  ::.::::::::::::.::                  %###*####            ")
        print("               #########                    ::::::::::::::.:::                   %#*****##          ")
        print("              %#######**#                    :::::::::::::.:::                   ####**####         ")
        print("              %#####%%%#**                   ::.::::::::::.:::                    %%#######         ")
        print("              %####%%#%###                   ::.::::::::::..::                    #%##%####         ")
        print("              %######%%###                    ::::::::::::..:                 #####%##%%####        ")
        print("             ############*                    ::..:::::::::::                 #%%%%%%#%%%###        ")
        print("             %######%%%##**                    ::::::::::.::                   %%%%%%%%%%%%        ")
    else:
        print("\n💀 The world falls into darkness...")


# =========================
# CLASS & SPELL SELECTION
# =========================
def choose_class():
    print("Choose your class:\n1. Warrior\n2. Mage\n3. Cleric\n4. Ogre")
    classes={"1":"warrior","2":"mage","3":"cleric","4":"ogre"}
    while True:
        choice=input("Enter 1-4: ")
        if choice in classes:
            return classes[choice]
        print("Invalid choice.")

def choose_starting_weapon(player):
    print("\nChoose your starting weapon:")
    weapons={"1":("Sword",5),"2":("Hammer",7),"3":("Staff",5),"4":("Dagger",3)}
    for k,(name,atk) in weapons.items():
        print(f"{k}. {name} (+{atk} attack)")
    while True:
        choice=input("Enter 1-4: ")
        if choice in weapons:
            player.weapon=weapons[choice]
            player.base_attack+=weapons[choice][1]
            print(f"You selected {weapons[choice][0]}! Base attack now {player.base_attack}.")
            break
        print("Invalid choice.")

def choose_starting_spell(player):
    print("\nChoose your starting spell:")
    spells=["Fireball","Ice Bolt","Healing Aura","Curse"]
    for i,spell in enumerate(spells):
        info=SPELLS_INFO[spell.lower()]
        print(f"{i+1}. {spell} - {info['desc']} ({info['mana']} Mana)")
    while True:
        choice=input("Enter 1-4: ")
        if choice in ["1","2","3","4"]:
            player.spells.append(spells[int(choice)-1].lower())
            print(f"You start with the spell: {spells[int(choice)-1]}!")
            break
        print("Invalid choice.")

# =========================
# MAIN GAME LOOP
# =========================
def main():
    while True:
        title_screen()
        show_intro()
        name = input("Enter your hero's name: ")
        player_class = choose_class()
        player = Player(name, player_class)
        choose_starting_weapon(player)
        choose_starting_spell(player)
        path = choose_path()
        resolve_path(path, player)
        again = input("\nPlay again? (yes/no): ").lower()
        if again!="yes":
            print("\nThanks for playing SHADOWS OF VALOR!")
            print("Written by Gary Oak")
            print("Buy me a coffee! https://www.buymeacoffee.com/garyoaktrees")
            break

main()