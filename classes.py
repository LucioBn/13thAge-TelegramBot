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
        'MD': 10
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
        'MD': 10
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
        'MD': 11
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
        'MD': 10
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
        'MD': 12
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
        'MD': 10
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
        'MD': 10
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
        'MD': 10
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
        'MD': 12
    }
}