classes = {
    'Barbarian': {
        'ability score': ['Str', 'Con'],
        'HP': 7,
        'AC': {
            'None': 10,
            'Light': 12,
            'Heavy': {
                'value': 13,
                'penalty': -2
                },
            'Shield': {
                'value': 1,
                'penalty': 0
            }
        },
        'PD': 11,
        'MD': 10,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 10
        },
        'Backgrounds': ['Clan Champion', 'Caravan Outrider', 'Fur Trapper', 'Mountain Tribeswoman', 'Wasteland Survivalist', 'Gladiator']
    },
    'Bard': {
        'ability score': ['Dex', 'Cha'],
        'HP': 7,
        'AC': {
            'None': 10,
            'Light': 12,
            'Heavy': {
                'value': 13,
                'penalty': -2
                },
            'Shield': {
                'value': 1,
                'penalty': -1
                },
        },
        'PD': 11,
        'MD': 10,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 8
        },
        'Backgrounds': ['Wandering Minstrel', 'Cathedral Musician', 'Court Jester', 'Mercenary', 'Tavern Owner', 'Failed Hedge Wizard', 'Diplomat', 'Spy', 'Royal Taster', 'Caravan Guide', 'Smuggler', 'Battle Skald']
    },
    'Cleric': {
        'ability score': ['Str', 'Wis'],
        'HP': 7,
        'AC': {
            'None': 10,
            'Light': 12,
            'Heavy': {
                'value': 14,
                'penalty': 0
                },
            'Shield': {
                'value': 1,
                'penalty': 0 
                },
        },
        'PD': 11,
        'MD': 11,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 8
        },
        'Backgrounds': ['Healer', 'Archivist', 'Military Chaplain', 'Temple Guard', 'Bartender', 'Reformed Thief', 'Dwarven Hierophant', 'Initiate', 'Bishop']
    },
    'Fighter': {
        'ability score': ['Str', 'Con'],
        'HP': 8,
        'AC': {
            'None': 10,
            'Light': 13,
            'Heavy': {
                'value': 15,
                'penalty': 0
                },
            'Shield': {
                'value': 1,
                'penalty': 0
                },
        },
        'PD': 10,
        'MD': 10,
        'Recoveries': 9,
        'Recovery Dice': {
            'times': 1,
            'faces': 10
        },
        'Backgrounds': ['Swordmaster', 'Mercenary Captain', 'Sea Raider', 'Shieldwall Spearman', 'Explorer', 'Bouncer', 'Thug', 'City Guardsman', 'Former Gladiator', 'Former Orc Captive', 'Bankrupt Nobleman', 'Duelist', 'Goblin-Hunter']
    },
    'Paladin': {
        'ability score': ['Str', 'Cha'],
        'HP': 8,
        'AC': {
            'None': 10,
            'Light': 12,
            'Heavy': {
                'value': 16,
                'penalty': 0
                },
            'Shield': {
                'value': 1,
                'penalty': 0
                },
        },
        'PD': 10,
        'MD': 12,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 10
        },
        'Backgrounds': ['City Guardsman', 'Combat Medic', 'Bodyguard', 'Outlaw Hunter', 'Inquisitor']
    },
    'Ranger': {
        'ability score': ['Str', 'Dex', 'Wis'],
        'HP': 7,
        'AC': {
            'None': 10,
            'Light': 14,
            'Heavy': {
                'value': 15,
                'penalty': 2
                },
            'Shield': {
                'value': 1,
                'penalty': 2
                },
        },
        'PD': 11,
        'MD': 10,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 8
        },
        'Backgrounds': ['Trackers', 'Bounty Hunters', 'Beast Slayers', 'Woodsy Assassins', 'Orc Slayers', 'Wanderers']
    },
    'Rogue': {
        'ability score': ['Dex', 'Cha'],
        'HP': 6,
        'AC': {
            'None': 11,
            'Light': 12,
            'Heavy': {
                'value': 13,
                'penalty': 2
                },
            'Shield': {
                'value': 1,
                'penalty': 2
                },
        },
        'PD': 12,
        'MD': 10,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 8
        },
        'Backgrounds': ['Street Thug', 'Cat Burglar', 'Diplomat', 'Professional Gambler', 'Courtier', 'Jewel Thief', 'Acrobat', 'Con Artist', 'Bartender', 'Spy Master', 'Pirate', 'Dandy', 'Rat Catcher']
    },
    'Sorcerer': {
        'ability score': ['Cha', 'Con'],
        'HP': 6,
        'AC': {
            'None': 10,
            'Light': 10,
            'Heavy': {
                'value': 11,
                'penalty': 2
                },
            'Shield': {
                'value': 1,
                'penalty': 2
                },
        },
        'PD': 11,
        'MD': 10,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 6
        },
        'Backgrounds': ['Tribal Shaman', 'Pirate Captain', 'Spell-Arena Gladiator', 'Failed Wizard', 'Sahuagin Hunter']
    },
    'Wizard': {
        'ability score': ['Int', 'Wis'],
        'HP': 6,
        'AC': {
            'None': 10,
            'Light': 10,
            'Heavy': {
                'value': 11,
                'penalty': 2
                },
            'Shield': {
                'value': 1,
                'penalty': 2
                },
        },
        'PD': 10,
        'MD': 12,
        'Recoveries': 8,
        'Recovery Dice': {
            'times': 1,
            'faces': 6
        },
        'Backgrounds': ['Magical Prodigy', 'Spell Thief', 'Hedge Wizard', 'Transformed Familiar', 'Shi\'s Wizard', 'Royal Poisoner']
    }
}