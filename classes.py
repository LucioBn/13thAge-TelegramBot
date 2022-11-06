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
        'Backgrounds': ['Clan Champion', 'Caravan Outrider', 'Fur Trapper', 'Mountain Tribeswoman', 'Wasteland Survivalist', 'Gladiator'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Club': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Hand-Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Warclub': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        },
                        'Battleaxe': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 10,
                            'atk': 0
                        },
                        'Greataxe': {
                            'times': 1,
                            'faces': 10,
                            'atk': 0
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': -5
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Spear': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': -5
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -5
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Str'], 'AC'],
                'Hit': ['Weapon', ['Str']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': 0
            }
        }
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
        'Backgrounds': ['Wandering Minstrel', 'Cathedral Musician', 'Court Jester', 'Mercenary', 'Tavern Owner', 'Failed Hedge Wizard', 'Diplomat', 'Spy', 'Royal Taster', 'Caravan Guide', 'Smuggler', 'Battle Skald'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Club': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Mace': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Shortsword': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        },
                        'Scimitar': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 10,
                            'atk': -2
                        },
                        'Dire flail': {
                            'times': 1,
                            'faces': 10,
                            'atk': -2
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -1
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Str', 'Dex'], 'AC'],
                'Hit': ['Weapon', ['Str', 'Dex']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': 0
            }
        }
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
        'Backgrounds': ['Healer', 'Archivist', 'Military Chaplain', 'Temple Guard', 'Bartender', 'Reformed Thief', 'Dwarven Hierophant', 'Initiate', 'Bishop'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Club': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Mace': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Shortsword': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        },
                        'Warhammer': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 10,
                            'atk': -2
                        },
                        'Dire flail': {
                            'times': 1,
                            'faces': 10,
                            'atk': -2
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': -2
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -1
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -5
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Str'], 'AC'],
                'Hit': ['Weapon', ['Str']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': 0
            }
        }
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
        'Backgrounds': ['Swordmaster', 'Mercenary Captain', 'Sea Raider', 'Shieldwall Spearman', 'Explorer', 'Bouncer', 'Thug', 'City Guardsman', 'Former Gladiator', 'Former Orc Captive', 'Bankrupt Nobleman', 'Duelist', 'Goblin-Hunter'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Club': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Hand Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Shortsword': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        },
                        'Warhammer': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 10,
                            'atk': 0
                        },
                        'Greataxe': {
                            'times': 1,
                            'faces': 10,
                            'atk': 0
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Str'], 'AC'],
                'Hit': ['Weapon', ['Str']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': 0
            }
        }
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
        'Backgrounds': ['City Guardsman', 'Combat Medic', 'Bodyguard', 'Outlaw Hunter', 'Inquisitor'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Club': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Scimitar': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Shortsword': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        },
                        'Battleaxe': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 10,
                            'atk': -2
                        },
                        'Halberd': {
                            'times': 1,
                            'faces': 10,
                            'atk': 0
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Str'], 'AC'],
                'Hit': ['Weapon', ['Str']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': 0
            }
        }
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
        'Backgrounds': ['Trackers', 'Bounty Hunters', 'Beast Slayers', 'Woodsy Assassins', 'Orc Slayers', 'Wanderers'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Club': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Scimitar': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Shortsword': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        },
                        'Battleaxe': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 10,
                            'atk': 0
                        },
                        'Halberd': {
                            'times': 1,
                            'faces': 10,
                            'atk': 0
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Str'], 'AC'],
                'Hit': ['Weapon', ['Str']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': 0
            }
        }
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
        'Backgrounds': ['Tribal Shaman', 'Pirate Captain', 'Spell-Arena Gladiator', 'Failed Wizard', 'Sahuagin Hunter'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Club': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Wicked Knife': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        },
                        'Shortsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': 0
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        },
                        'Scimitar': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        },
                        'Axe': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -1
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': -1
            }
        }
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
        'Backgrounds': ['Magical Prodigy', 'Spell Thief', 'Hedge Wizard', 'Transformed Familiar', 'Shi\'s Wizard', 'Royal Poisoner'],
        'Weapons': {
            'Melee Weapons': {
                'Small': {
                    'One-Handed': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Two-Handed': {
                        'Staff': {
                            'times': 1,
                            'faces': 6,
                            'atk': 0
                        }
                    }
                },
                'Light or Simple': {
                    'One-Handed': {
                        'Shortsword': {
                            'times': 1,
                            'faces': 6,
                            'atk': -2
                        }
                    },
                    'Two-Handed': {
                        'Spear': {
                            'times': 1,
                            'faces': 8,
                            'atk': -2
                        }
                    },
                },
                'Heavy or Martial': {
                    'One-Handed': {
                        'Longsword': {
                            'times': 1,
                            'faces': 8,
                            'atk': -5
                        }
                    },
                    'Two-Handed': {
                        'Greatsword': {
                            'times': 1,
                            'faces': 10,
                            'atk': -5
                        }
                    }
                }
            },
            'Ranged Weapons': {
                'Small': {
                    'Thrown': {
                        'Dagger': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Crossbow': {
                        'Hand Crossbow': {
                            'times': 1,
                            'faces': 4,
                            'atk': 0
                        }
                    },
                    'Bow': None
                },
                'Light or Simple': {
                    'Thrown': {
                        'Javelin': {
                            'times': 1,
                            'faces': 6,
                            'atk': -2
                        }
                    },
                    'Crossbow': {
                        'Light Crossbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': -1
                        }
                    },
                    'Bow': {
                        'Shortbow': {
                            'times': 1,
                            'faces': 6,
                            'atk': -2
                        }
                    }
                },
                'Heavy or Martial': {
                    'Thrown': None,
                    'Crossbow': {
                        'Heavy Crossbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -4
                        }
                    },
                    'Bow': {
                        'Longbow': {
                            'times': 1,
                            'faces': 8,
                            'atk': -5
                        }
                    }
                }
            }
        },
        'Basic Attacks': {
            'Melee attack': {
                'Target': 'One enemy',
                'Attack': [['Str'], 'AC'],
                'Hit': ['Weapon', ['Str']],
                'Miss': -1
            },
            'Ranged attack': {
                'Target': 'One enemy',
                'Attack': [['Dex'], 'AC'],
                'Hit': ['Weapon', ['Dex']],
                'Miss': 0
            }
        }
    }
}