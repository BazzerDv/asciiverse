#!/usr/bin/python3

import os, random
import curses
from curses import *
import time

run = True
menu = True
play = False
rules = False
fight = False
standing = True
buy = False
speak = False
boss = False


def new():
    global HP, HPMAX, ATK, gems, discovered, pot, elix, gold, gpersec, x, y, equipped_weap, equipped_armour, key
    HP = 50
    HPMAX = HP
    ATK = 1
    pot = 5
    elix = 0
    gold = 0
    x = 0
    y = 0
    discovered = False
    key = False
    gems = 0
    equipped_weap = 'Fists'
    equipped_armour = 'None'
    gpersec = 1
    
new()

def convert(s):
    if s.strip() == 'True':
        return True
    return False

map1 = [["plains", "plains", "plains", "plains", "forest", "mountain", "cave"],
       ["forest", "forest", "forest", "forest", "forest", "hills", "mountain"],
       ["forest", "fields", "bridge", "plains", "hills", "forest", "hills"],
       ["plains", "shop", "town", "mayor", "plains", "hills", "mountain"],
       ["plains", "fields", "fields", "plains", "hills", "mountain", "mountain"]]

map = [['hut', 'fields', 'plains', 'plains', 'mayor', 'forest', 'portal'],
       ['fields', 'fields', 'shop', 'plains', 'forest','forest', 'mountain'],
       ['plains', 'plains', 'forest', 'forest', 'forest', 'mountain', 'mountain'],
       ['plains', 'forest', 'forest', 'forest', 'forest', 'mountain', 'cave'],
       ['plains', 'plains', 'forest', 'forest', 'mountain', 'mountain', 'mountain']]

y_len = len(map)-1
x_len = len(map[0])-1

biome = {
    "plains": {
        "t": "PLAINS",
        "e": True,
        'enemies':['Slime']
        },
    'wall': {
        'e': False
        },
    "forest": {
        "t": "WOODS",
        "e": True,
        'enemies': ['Bear']
        },
    'hut': {
        't': 'HUT',
        'e': False
        },
    "fields": {
        "t": "FIELDS",
        "e": False
        },
    "bridge": {
        "t": "BRIDGE",
        "e": True
        },
    "town": {
        "t": "TOWN CENTRE",
        "e": False
        },
    "shop": {
        "t": "SHOP",
        "e": False},
    "mayor": {
        "t": "MAYOR",
        "e": False
        },
    "cave": {
        "t": "CAVE",
        "e": False
        },
    "mountain": {
        "t": "MOUNTAINS",
        "e": True,
        'enemies': ['Goblin', 'Orc']
        },
    "hills": {
        "t": "HILLS",
        "e": True
        },
    'portal': {
        't': 'PORTAL',
        'e': False
        }
    }

e_list = ['Goblin', 'Orc', 'Slime']

mobs = {
    'Goblin': {
        'hp': 50,
        'at': 15,
        'go': 75,
        'drop': 'Goblin Hat',
        'type': 'item',
        'chance': 400
        },
    
    'Orc': {
        'hp': 100,
        'at': 30,
        'go': 1000,
        'drop': 'Club',
        'type': 'weapon',
        'chance': 30
        },
    'Slime': {
        'hp': 15,
        'at': 2,
        'go': 20,
        'drop': 'Liquidised Slime',
        'type': 'item',
        'chance': 75
        },
    'Bear': {
        'hp': 30,
        'at': 7,
        'go': 100,
        'drop': 'Bear Skin',
        'type': 'armour',
        'chance': 65
        }
    }

bosses = {
    'Dragon': {
        'hp': 500,
        'at': 50,
        'go': 100,
        'drop': "Dragon's Bane",
        'type': 'weapon',
        'chance': 20
        }
    }
symbols = {
    'plains': ',,,',
    'forest': '888',
    'fields': '...',
    'hills': 'nnn',
    'shop': ' S ',
    'mayor': ' M ',
    'cave': ' C ',
    'mountain': '/^\x5c',
    'bridge': '===',
    'town': ' T ',
    'hut': ' H ',
    'portal': ' P '
    }


weapons = {
    'Fists': {
        'dmg': 1,
        'acq': True
        },
    'Wooden Sword': {
        'dmg': 3,
        'acq': False
        },
    'Iron Sword': {
        'dmg': 5,
        'acq': False
        },
    'Club': {
        'dmg': 8,
        'acq': False
        },
    'Diamond Sword': {
        'dmg': 10,
        'acq': False
        },
    "Dragon's Bane": {
        'dmg': 20,
        'acq': False
        }
    }
    
acq_weapons = ['Fists']

armours = {
    'None': {
        'arm': 0,
        'acq': True
        },
    'Wooden Armour': {
        'arm': 3,
        'acq': False
        },
    'Bear Skin': {
        'arm': 5,
        'acq': False
        },
    'Iron Armour': {
        'arm': 6,
        'acq': False
        },
    'Diamond Armour': {
        'arm': 10,
        'acq': False
        }
    }

acq_armour = ['None']
invent = {
    'Liquidised Slime': {
        'acq': False,
        'description': '(+3g/s)'
        },
    'Goblin Hat': {
        'acq': False,
        'description': '(+25HP)'
        }
    }

ascii_map = [['', '', '', '', '', '', ''],
             ['', '', '', '', '', '', ''],
             ['', '', '', '', '', '', ''],
             ['', '', '', '', '', '', ''],
             ['', '', '', '', '', '', '']]

shop_equipment = {
    'weapons': {
        'Wooden Sword': 150,
        'Iron Sword': 500,
        'Diamond Sword': 2000
        },
    'armour': {
        'Wooden Armour': 200,
        'Iron Armour': 600,
        'Diamond Armour': 2500
        }
    }
    
shop_arm_keys = list(shop_equipment['armour'])
shop_weap_keys = list(shop_equipment['weapons'])
last_bought_arm = 'None'
last_bought_weap = 'None'
current_tile = map[y][x]
name_of_tile = biome[current_tile]["t"]
enemy_tile = biome[current_tile]["e"]

def clear():
    os.system("clear")

def draw():
    print("Xx" + "-"*30 + "xX")

def draw_map():
    global ascii_map, discovered
    for i in range(len(map)):
        for j in range(len(map[i])):
            ascii_map[i][j] = symbols[map[i][j]]
            if map[i][j] == 'portal'and not discovered:
                ascii_map[i][j] = '???'
    ascii_map[y][x] = '\x5c'+'o/'

    
def save():
    global discovered, key
    list = [
        name,
        str(HP),
        str(ATK),
        str(pot),
        str(elix),
        str(gold),
        str(x),
        str(y),
        str(gems),
        str(equipped_weap),
        str(equipped_armour),
        str(key),
        str(discovered),
        str(gpersec),
        str(HPMAX),
        str(last_bought_weap),
        str(last_bought_arm)
        ]
    with open("game_data.txt", "w") as f:
        for item in list:
            f.write(item + "\n")

    list = []
    for weapon in weapons:
        list.append(str(weapons[weapon]['acq']))
    with open('weapons.txt', 'w') as f:
        for item in list:
            f.write(item + '\n')

    list = []        
    for armour in armours:
        list.append(str(armours[armour]['acq']))
    with open('armours.txt', 'w') as f:
        for item in list:
            f.write(item + '\n')

    list = []        
    for item in invent:
        list.append(str(invent[item]['acq']))
    with open('items.txt', 'w') as f:
        for string in list:
            f.write(string + '\n')
    
    
def battle():
    global fight, play, run, HP, HPMAX, pot, elix, gold, hut_dialogue, invent, boss, gpersec

    if not boss:
        enemy = random.choice(biome[map[y][x]]['enemies'])
        hp = mobs[enemy]['hp']
        hpmax = hp
        atk = mobs[enemy]['at']
        g = mobs[enemy]['go']
        drop = mobs[enemy]['drop']
        drop_chance = mobs[enemy]['chance']
    else:
        enemy = 'Dragon'
        hp = bosses[enemy]['hp']
        hpmax = hp
        atk = bosses[enemy]['at']
        g = bosses[enemy]['go']
        drop = bosses[enemy]['drop']
        drop_chance = bosses[enemy]['chance']
    

    while fight:
        clear()
        draw()
        print('Defeat the ' + enemy + '!')
        draw()
        print(enemy + "'s HP: " + str(hp) + '/' + str(hpmax))
        print(name + "'s HP: " + str(HP) + '/' + str(HPMAX))
        print('POTION(S): ' + str(pot))
        print('ELIXIR: ' + str(elix))
        draw()
        print('1 - ATTACK')
        if pot > 0:
            print('2 - USE POTION (+30HP)')
        if elix > 0:
            print('3 - USE ELIXIR (+50HP)')
        draw()

        choice = input('# ')

        if choice == '1':
            hp -= weapons[equipped_weap]['dmg']
            if hp < 0:
                hp = 0
            print(name + ' dealt ' + str(ATK) + ' damage to the ' + enemy + '.')
            if hp > 0:
                if atk - armours[equipped_armour]['arm'] > 0:
                    HP -= atk - armours[equipped_armour]['arm']
                    damage = atk - armours[equipped_armour]['arm']
                else:
                    HP -= 0
                    damage = 0
                print(enemy + ' dealt ' + str(damage) + ' damage to ' + name + '.')
                input('> ')
                
        elif choice == '2':
            if pot > 0:
                pot -= 1
                HP += 30
                if HP > HPMAX:
                    HP = HPMAX
                print('You used a potion. (+30HP)')
        elif choice == '3':
            if elix > 0:
                elix -= 1
                HP += 50
                if HP > HPMAX:
                    HP = HPMAX

        if HP <= 0:
            print(enemy + ' defeated ' + name + '...')
            draw()
            fight = False
            print('The world turns black...')
            input('> ')
            hut_dialogue = True
            HP = HPMAX
            hut()

        if hp <= 0:
            print(name + ' defeated ' + enemy + '!')
            draw()
            fight = False
            gold += g
            print("You found " + str(g) + ' gold')
            if random.randint(0, 100) < 30:
                pot += 1
                print('You found a potion!')
            if random.randint(0, 100) < 5:
                elix += 1
                print('You found an elixir!')

            if random.randint(0, 100) < drop_chance:
                if mobs[enemy]['type'] == 'weapon':
                    if not weapons[mobs[enemy]['drop']]['acq']:
                        weapons[mobs[enemy]['drop']]['acq'] = True
                        print('You found ' + drop)
                if mobs[enemy]['type'] == 'armour':
                    if not armours[mobs[enemy]['drop']]['acq']:
                        armours[mobs[enemy]['drop']]['acq'] = True
                        print('You found ' + drop)
                if mobs[enemy]['type'] == 'item':
                    if not invent[mobs[enemy]['drop']]['acq']:
                        invent[mobs[enemy]['drop']]['acq'] = True
                        if invent['Liquidised Slime']['acq']:
                            gpersec += 3
                        print('You found ' + drop)
            if enemy == 'Dragon':
                draw()
                print('Congratulations!\nYou defeated the dragon!\nYou have gained a gem...')
                boss = False
                fight = False
            input('> ')
            clear()

def inventory():
    global invent, equipped_armour, equipped_weap, armours, weapons
    inv = True
    while inv:
        count = 0
        clear()
        print('INVENTORY')
        draw()
        print('WEAPON: ' + equipped_weap)
        print('ARMOUR: ' + equipped_armour)
        draw()
        for item in invent:
            if invent[item]['acq']:
                print('{} {}'.format(item, invent[item]['description']))
                count += 1
        if count == 0:
            print('YOU HAVE NO ITEMS IN YOUR INVENTORY')
            
        draw()
        print('1 - BACK')
        print('2 - CHANGE WEAPON')
        print('3 - CHANGE ARMOUR')
        draw()
        choice = input('# ')
        
        if choice == '1':
            inv = False

        if choice == '2':
            count = 0
            input_keys = {}
            clear()
            weap_list = list(weapons)
            draw()
            for i in range(len(weapons)):
                if weapons[weap_list[i]]['acq']:
                    count += 1
                    input_keys[str(count)] = weap_list[i]
                    print('{} - {}'.format(str(count), weap_list[i]))
            draw()
            choice = input('# ')
            picked = False
            while not picked:
                if choice in input_keys:
                    equipped_weap = input_keys[choice]
                    print('You equipped {}'.format(equipped_weap))
                    picked = True
            input('> ')

        elif choice == '3':
            count = 0
            input_keys = {}
            clear()
            arm_list = list(armours)
            draw()
            for i in range(len(armours)):
                if armours[arm_list[i]]['acq']:
                    count += 1
                    input_keys[str(count)] = arm_list[i]
                    print('{} - {}'.format(str(count), arm_list[i]))

            draw()
            choice = input('# ')
            picked = False
            while not picked:
                if choice in input_keys:
                    equipped_armour = input_keys[choice]
                    print('You equipped {}'.format(equipped_armour))
                    picked = True
            input('> ')
def shop():
    global buy, gold, pot, elix, ATK, last_bought_arm, last_bought_weap, shop_weap_keys, shop_arm_keys

    while buy:
        clear()
        draw()
        print('Welcome to the shop!')
        draw()
        print('GOLD: ' + str(gold))
        print('POTIONS: ' + str(pot))
        print('ELIXIRS: '+ str(elix))
        print('ATK: ' + str(ATK))
        draw()
        print('1 - BUY POTION (30HP) - 100')
        print('2 - BUY ELIXIR (50HP) - 50')
        
        if last_bought_weap == 'None':
            print('3 - BUY WOODEN SWORD - 150')
            sword_name = 'Wooden Sword'
            weap_price = 150
        elif last_bought_weap == 'Diamond Sword':
            print('   ---')
        else:
            new_last_w = shop_weap_keys.index(last_bought_weap)
            new_last_w += 1
            sword_name = shop_weap_keys[new_last_w]
            weap_price = shop_equipment['weapons'][sword_name]
            print('3 - BUY ' + sword_name.upper() + ' - ' + str(weap_price))

        if last_bought_arm == 'None':
            print('4 - BUY WOODEN ARMOUR - 200')
            armour_name = 'Wooden Armour'
            arm_price = 200
        elif last_bought_arm == 'Diamond Armour':
            print('   ---')
        else:
            new_last_a = shop_arm_keys.index(last_bought_arm)
            new_last_a += 1
            armour_name = shop_arm_keys[new_last_a]
            arm_price = shop_equipment['armour'][armour_name]
            print('4 - BUY ' + armour_name.upper() + ' - ' + str(shop_equipment['armour'][armour_name]))
        print('5 - LEAVE')
        draw()

        choice = input('# ')

        if choice == '1':
            if gold >= 100:
                pot += 1
                gold -= 100
                print('You bought a potion')
            else:
                print('Not enough gold!')
            input()
        if choice == '2':
            if gold >= 500:
                elixir += 1
                gold -= 500
                print('You bought an elixir')
            else:
                print('Not enough gold!')

        if choice == '3':
            if last_bought_weap != 'Diamond Sword':
                if gold >= weap_price:
                    gold -= weap_price
                    weapons[sword_name]['acq'] = True
                    last_bought_weap = sword_name
                    print('You bought a(n) ' + sword_name.lower())
                else:
                    print('Not enough gold!')
            else:
                print('I have no more swords to sell to you')
            input('> ')

        if choice == '4':
            if last_bought_arm != 'Diamond Sword':
                if gold >= arm_price:
                    gold -= arm_price
                    armours[armour_name]['acq'] = True
                    last_bought_arm = armour_name
                    print('You bought a(n) ' + armour_name.lower())
                else:
                    print('Not enough gold!')
            else:
                print('I have no more armour to sell to you')
        if choice == '5':
            buy = False

def mayor():
    global speak, key
    clear()
    draw()
    print('Hello there, ' + name + '!')
    if ATK < 10:
        print("You're not ready to face the dragon yet, come back when you are stronger!")
        key = False
    else:
        print("Here's the key to the dragon's lair! Be careful!")
        key = True
    draw()
    print('1 - LEAVE')
    draw()

    choice = input('# ')

    if choice == '1':
        speak = False

def cave():
    global boss, key, fight

    while boss:
        clear()
        draw()
        print('Here lies the cave of the dragon. What will you do?')
        draw()
        if key:
            print('1 - USE KEY')
            
        print('2 - TURN BACK')
        draw()

        choice = input('# ')

        if choice == '1':
            if key:
                fight = True
                battle()
        elif choice == '2':
            boss = False

def portal():
    global gems
    clear()
    draw()
    print('PORTAL')
    draw()
    print('You see what seems to be the\nremnants of a portal, built\nfrom a purply-black material.')
    print('There appears to be a slot for\nsomething like... a gem?')
    draw()
    if gems >= 1:
        print('1 - PLACE GEM')
    else:
        print('   ---')
    print('2 - LEAVE')
    
    draw()
    choice = input('# ')
    
    if choice == '1':
        if gems >= 1:
            print('You place the gem in the slot, and the portal fizzes to life')
            input('> ')
            clear()
            print('You step into the portal...')
            print("""     *  __________
       / ________ *
      / / ______ \x5c
     / / /  ___ \x5c*\x5c
     | | | / _ \x5c \x5c \x5c
  *  | | | ||*|| | |    
     | |*| \__/| | |   
     \ \ \_____/ / /   *
      \ \_______/ /
  *    \_________/
                *
          
          *
          """)
            input('> ')
            
def hut():
    global HP, HPMAX, hut_dialogue, x, y
    x = 0
    y = 0
    while hut_dialogue:
        clear()
        draw()
        print('HUT')
        draw()
        print('What can I do for you?')
        draw()

        print('1 - Can i rest here?')
        print('2 - What happened?')
        print('3 - Leave')
        draw()

        choice = input('# ')

        if choice == '1':
            clear()
            draw()
            print('HUT')
            draw()
            print('Sure thing!')
            draw()
            HP = HPMAX
            print('You are fully rested')
            input('> ')
        elif choice == '2':
            clear()
            draw()
            print('HUT')
            draw()
            print('I found you left for dead in the forest, and for the last year I have been looking after you while you were in a coma')
            draw()
            print('1 - Thanks!')
            print("2 - You should feel honoured")
            draw()
            choice = input('# ')
            if choice == '1':
                clear()
                draw()
                print('HUT')
                draw()
                print("No problem.")
                draw()
                input('> ')
            elif choice == '2':
                clear()
                draw()
                print('HUT')
                draw()
                print("That's rude of you!")
                draw()
                print('1 - Sorry...')
                draw()
                choice = input('# ')
                if choice == '1':
                    clear()
                    draw()
                    print('HUT')
                    draw()
                    print("It's okay. Don't let it happen again")
                    draw()
                    input('> ')
        elif choice == '3':
            hut_dialogue = False
            clear()
while run:            
    while menu:
        clear()
        print("""                                 _ _
                                (_|_)
                    __ _ ___ ___ _ __   ______ __ ___  ___
                   / _` / __| __| |\ \ / / _ \x5c' _/ __|/ _ \x5c
                  | (_| \__ \(__| | \ V /  __/ | \__ \  __/
                   \__,_|___/___|_|_|\_/ \___|_| |___/\___|
 """)
        print(' '*22, end='')
        draw()
        print(' '*33 +"1, NEW GAME")
        print(' '*33 +"2, LOAD GAME")
        print(' '*33 +"3, RULES")
        print(' '*33 +"4, QUIT GAME")
        print(' '*22, end='')
        draw()
        
        if rules:
            print("I'm the creator of this game and here are the rules:")
            rules = False
            choice = ""
            input("> ")
        else:
            choice = input("                                # ")
            
        if choice == "1":
            clear()
            new()
            name = input("# What's your name, adventurer? ")
            hut_dialogue = True
            hut()
            menu = False
            play = True
            

        elif choice == "2":
            try:
                f = open("game_data.txt", "r")
                load_list = f.readlines()
                fw = open('weapons.txt', 'r')
                load_listw = fw.readlines()
                fa = open('armours.txt', 'r')
                load_lista = fa.readlines()
                fi = open('items.txt', 'r')
                load_listi = fi.readlines()
                if len(load_list) == 17 and len(load_listw) == len(weapons) and len(load_lista) == len(armours) and len(load_listi) == len(invent):
                    name = load_list[0][:-1]
                    HP = int(load_list[1][:-1])
                    #ATK = int(load_list[2][:-1])
                    pot = int(load_list[3][:-1])
                    elix = int(load_list[4][:-1])
                    gold = int(load_list[5][:-1])
                    x = int(load_list[6][:-1])
                    y = int(load_list[7][:-1])
                    gems = int(load_list[8][:-1])
                    equipped_weap = load_list[9][:-1]
                    equipped_armour = load_list[10][:-1]
                    ATK = int(weapons[equipped_weap]['dmg'])
                    key = convert(load_list[11][:-1])
                    discovered = convert(load_list[12][:-1])
                    gpersec = int(load_list[13][:-1])
                    HPMAX = int(load_list[14][:-1])
                    last_bought_weap = load_list[15][:-1].strip()
                    last_bought_arm = load_list[16][:-1].strip()
                    clear()
                    print("Welcome back, " + name)
                    menu = False
                    play = True

                    i = 0
                    for weapon in weapons:
                        weapons[weapon]['acq'] = convert(load_listw[i][:-1])
                        i += 1
                        
                    i = 0
                    for armour in armours:
                        armours[armour]['acq'] = convert(load_lista[i][:-1])
                        i += 1

                    i = 0
                    for item in invent:
                        invent[item]['acq'] = convert(load_listi[i][:-1])
                        i += 1

                    
                else:
                    print("Your save files are corrupt!")

            except IOError:
                print("You do not have any save data that can be loaded")
            input('> ')
        elif choice == "3":
            rules = True

        elif choice == "4":
            quit()

    start_time = time.time()
    elapsed_time = 0
    while play:
        elapsed_time += time.time() - start_time
        if elapsed_time > 1:
            gold += gpersec*(int(elapsed_time//1))
            elapsed_time = 0
            start_time = time.time()
        save()
        clear()
        
        if not standing:
            if biome[map[y][x]]['e']:
                if random.randint(0,100) <= 33:
                    fight = True
                    battle()

        if play:
            draw_map()
            space = ' '*20
            draw()
            print("LOCATION: " + biome[map[y][x]]["t"])
            draw()
            print('NAME: ' + name)
            spaces = len(str(HP)) + len(str(HPMAX))
            if spaces < 13:
                spaces = 13 - spaces
                spaces = spaces + 1
                spaces += 13
            print('HP: ' + str(HP) + '/' + str(HPMAX) + ' '*spaces, (*ascii_map[0]))
            print('ATK: ' +str(weapons[equipped_weap]['dmg']) + space + '      ', (*ascii_map[1]))
            print('POTION(S): ' + str(pot) + space, (*ascii_map[2]))
            print('ELIXIR: ' + str(elix) + space + '   ', (*ascii_map[3]))
            print('GOLD: ' + str(gold) + space + '     ', (*ascii_map[4]))
            print('GOLD PER SEC: {}'.format(int(gpersec)))
            print('COORDINATES: ' + str(x) + ', ' + str(y))
            draw()
            print("0 - SAVE AND QUIT")
            
            if y > 0:
                print("1 - NORTH")
                north = True
            else:
                print('---')
                north = False
                
            if x < x_len:
                print("2 - EAST")
                east = True
            else:
                print(' ---')
                east = False
                
            if y < y_len:
                print("3 - SOUTH")
                south = True
            else:
                print(' ---')
                south = False
                
            if x > 0:
                print("4 - WEST")
                west = True
            else:
                print(' ---')
                west =  False

            if pot > 0:
                print('5 - USE POTION (+30HP)')
            else:
                print(' ---')
                
            if elix > 0:
                print('6 - USE ELIXIR (+50HP)')
            else:
                print(' ---')

            print('7 - INVENTORY')

            if map[y][x] == 'shop' or map[y][x] == 'portal' or map[y][x] == 'mayor' or map[y][x] == 'cave' or map[y][x] == 'hut':
                print('8 - ENTER')
                
            draw()
            
            dest = input("# ")

            if dest == "0":
                play = False
                menu = True
                save()

            elif dest == '1':
                if north:
                    y -= 1
                    standing = False
    ##            if y > 0:
    ##                y -= 1
    ##            else:
    ##                y = y_len
            elif dest == '2':
                if east:
                    x += 1
                    standing = False
    ##            if x < x_len:
    ##                x += 1
    ##            else:
    ##                x = 0

            elif dest == '3':
                if south:
                    y += 1
                    standing = False
    ##            if y < y_len:
    ##                y += 1
    ##            else:
    ##                y = 0
            elif dest == '4':
                if west:
                    x -= 1
                    standing = False
    ##            if x > 0:
    ##                x -= 1
    ##            else:
    ##                x += 1
            elif dest == '5':
                if pot > 0:
                    pot -= 1
                    HP += 30
                    if HP > HPMAX:
                        HP = HPMAX
                standing = True

            elif dest == '6':
                if elix > 0:
                    elix -= 1
                    HP += 50
                    if HP > HPMAX:
                        HP = HPMAX
                standing = True

            elif dest == '7':
                inventory()
                standing = True

            elif dest == '8':
                if map[y][x] == 'shop':
                    buy = True
                    shop()
                if map[y][x] == 'mayor':
                    speak = True
                    mayor()
                if map[y][x] == 'cave':
                    boss = True
                    cave()
                if map[y][x] == 'portal':
                    discovered = True
                    portal()
                if map[y][x] == 'hut':
                    hut_dialogue = True
                    hut()
            else:
                standing = True
