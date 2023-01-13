monsters = {
    "ANIMAL / CRITTER": {
        "Monster": False,

        "Dire features (d6)": {
            1: "Armor plates—Add +2 to the dire animal’s AC, and add +1 to its PD.",
            2: "Spiky bits—Whenever an enemy hits the dire animal with a melee attack, deal damage equal to twice the animal’s level to that attacker.",
            3: "Carnage—The dire animal’s attacks that miss deal damage equal to its level. When staggered, its missed attacks deal damage equal to double its level.",
            4: "Poison—The dire animal’s main attack also deals 5 ongoing poison damage per tier (5 ongoing poison at levels 1–4, 10 at 5–7, etc.).",
            5: "Dire regeneration—When the escalation die is even, this animal heals damage equal to triple its level at the start of its turn.",
            6: "Fury—While staggered, the dire animal gains a +2 attack bonus and deals +4 damage, but at the end of each of its turns it takes 2d6 damage."
        },

        "Giant Ant": {
            "Size": "Normal",
            "Level": 0,
            "Monster Role": "Wrecker",
            "Type": "Beast",
            "IB": 6,
            "Attack": {
                "Mandibles +5 vs. AC": "3 damage\nNatural 16+: The target also takes 1d3 ongoing acid damage.",
                "Wall-crawler": "A giant ant can climb on ceilings and walls as easily as it moves on the ground."
            },
            "AC": 14,
            "PD": 13,
            "MD": 9,
            "HP": 20
        },

        "Giant Scorpion": {
            "Size": "Normal",
            "Level": 1,
            "Monster Role": "Wrecker",
            "Type": "Beast",
            "IB": 0,
            "Attack": {
                "Pincer +6 vs. PD": "1 damage, and the scorpion gains a +2 attack bonus against the same target this turn with its stinger attack.\nLimited use: 2/round, each requiring a quick action. (Hitting the same target twice with pincer gives the stinger attack a +4 bonus).",
                "Stinger +6 vs. AC": "3 damage, and 3 ongoing poison damage."
            },
            "AC": 16,
            "PD": 15,
            "MD": 10,
            "HP": 22
        },

        "Hunting Spider": {
            "Size": "Normal",
            "Level": 2,
            "Monster Role": "Wrecker",
            "Type": "Beast",
            "IB": 6,
            "Attack": {
                "Bite +6 vs. AC": "8 damage\nNatural 16+: The target also takes 1d8 ongoing poison damage.",
                "Scuttle": "A hunting spider can turn its own failed disengage check into a success by taking 1d4 damage.",
                "Wall-crawler": "A hunting spider can climb on ceilings and walls as easily as it moves on the ground."
            },
            "AC": 17,
            "PD": 14,
            "MD": 11,
            "HP": 34
        },

        "Bear": {
            "Size": "Normal",
            "Level": 2,
            "Monster Role": "Troop",
            "Type": "Beast",
            "IB": 4,
            "Attack": {
                "Bite +7 vs. AC": "6 damage.\nNatural even hit: The target takes +1d6 damage from a claw swipe."
            },
            "AC": 17,
            "PD": 16,
            "MD": 12,
            "HP": 45
        },

        "Dire Bear": {
            "Size": "Large",
            "Level": 4,
            "Monster Role": "Troop",
            "Type": "Beast",
            "IB": 7,
            "Attack": {
                "Bite +8 vs. AC": "24 damage.\nNatural even hit: The target takes +2d6 damage from a claw swipe.",
                "Savage": "The dire bear gains a +2 attack bonus against staggered enemies.",
                "One dire feature": "Roll randomly unless you know this beast’s story already."
            },
            "AC": 19,
            "PD": 19,
            "MD": 14,
            "HP": 130
        }
    },

    "BULLETTE": {
        "Monster": True,

        "Size": "Large",
        "Level": 5,
        "Monster Role": "Wrecker",
        "Type": "Beast",
        "IB": 7,
        "Attack": {
            "Gigantic claws +12 vs. AC (2 attacks)": "15 damage.\nDual hit: If both claws hit during the same turn, the bulette can make a terrible bite attack during its next turn as a standard action.",
            "[Special trigger] Terrible bite +14 vs. AC": "45 damage.\nMiss: 22 damage.",
            "Blood frenzy": "The bulette’s crit range expands to 16+ while the escalation die is 4+.",
            "Serious burrower": "A bulette can burrow incredibly quickly for short distances. They’re renowned for the mounds of dirt and rock they push above them as they surge through the ground like land torpedoes (see page 200 for burrow rules).",
            "Nastier Specials\nSavage response": "When an attacker scores a critical hit against the bulette and it survives, the bulette can make a terrible bite attack as a free action against one target engaged with it."
        },
        "AC": 22,
        "PD": 19,
        "MD": 14,
        "HP": 170
    },

    "CHIMERA": {
        "Monster": True,

        "Size": "Large",
        "Level": 9,
        "Monster Role": "Wrecker",
        "Type": "Beast",
        "IB": 15,
        "Attack": {
            "Fangs, claws, and horns +14 vs. AC (3 attacks)": "25 damage.\nNatural 14–15: The target is dazed until the end of the chimera’s next turn from a headbutt.\nNatural 16–17: The target takes 20 ongoing damage from raking claws.\nNatural 18–20: The chimera makes a fiery breath attack as a free action.",
            "[Special trigger] Fiery breath +14 vs. PD (up to 3 nearby enemies in a group)": "3d10 fire damage.",
            "Bestial thresher": "Whenever a creature misses the chimera with a melee attack, the chimera’s multiple sharp bits deal 3d10 damage to that attacker.",
            "Serious burrower": "A bulette can burrow incredibly quickly for short distances. They’re renowned for the mounds of dirt and rock they push above them as they surge through the ground like land torpedoes (see page 200 for burrow rules).",
            "Nastier Specials\nNow it’s angry": "When an attacker scores a critical hit against the chimera and it survives, its attack rolls on its next turn deal the effects of the lower rolls as well as their own results; for example, a roll of 18–20 would daze the target and deal 20 ongoing damage as well as triggering fiery breath."
        },
        "AC": 24,
        "PD": 20,
        "MD": 16,
        "HP": 320
    },
    
    "DEMON": {
        "Monster": False,

        "Random Demon Abilities (d6 or d8)": {
            1: "True seeing—The demon is immune to invisibility and ignores any illusions.",
            2: "Resist fire 18+—You’ll see that the demon resists fire the first time you use fire against it.",
            3: "Invisibility—The first time the demon is staggered each battle it becomes invisible until the end of its next turn.",
            4: "Resist energy 12+—The demon’s resistance to all energy types puts a damper on enemy spellcasters, but at least the resistance is only 12+.",
            5: "Fear aura—Enemies engaged with the demon who are below its fear hit point threshold are dazed and can’t use the escalation die; see Fear level thresholds on page 200.",
            6: "Teleport 1d3 times each battle—As a move action, the demon can teleport anywhere it can see nearby.",
            7: "Demonic speed—The demon can take an extra action each turn while the escalation die is 4+.",
            8: "Gate—Once per battle as a standard action, if the demon is staggered, it can summon a single demon ally at least two levels below its own level. The allied demon rolls initiative and does not appear on the battlefield until its turn starts. (Note that using a gate costs the demon an obligation, so some demons would rather flee or die than activate one)."
        },

        "Imp": {
            "Size": "Normal",
            "Level": 3,
            "Monster Role": "Spoiler",
            "Type": "Demon",
            "IB": 8,
            "Attack": {
                "Festering claws +7 vs. AC": "3 damage, and 5 ongoing damage.",
                "R: Blight jet +7 vs. PD": "7 damage, and the target is dazed (save ends).\nFirst natural 16+ each turn: The imp can choose one: the target is weakened instead of dazed; OR the imp can make a blight jet attack against a different target as a free action.",
                "Curse aura": "Whenever a creature attacks the imp and rolls a natural 1–5, that creature takes 1d10 psychic damage.",
                "Flight": "Imps are hard to pin down because they fly. Not that fast or well, but you don’t have to fly well to fly better than humans and elves."
            },
            "AC": 20,
            "PD": 13,
            "MD": 16,
            "HP": 40
        },

        "Despoiler": {
            "Size": "Normal",
            "Level": 4,
            "Monster Role": "Caster",
            "Type": "Demon",
            "IB": 9,
            "Attack": {
                "Horns and daggers +8 vs. AC (2 attacks)": "5 damage.\nNatural 16+: The despoiler can pop free from the target.",
                "R: Abyssal whispers +9 vs. MD (one nearby or far away enemy)": "15 psychic damage, and the target is confused (save ends); OR the target can choose to avoid the confusion effect by taking 6d6 psychic damage to clear their head . . .",
                "C: Sow discord +9 vs. MD (2 nearby enemies engaged with the same creature or with each other)": "one target makes an at-will melee attack against this power’s other target.\nLimited use: 1/day, as a quick action."
            },
            "AC": 19,
            "PD": 14,
            "MD": 18,
            "HP": 52
        },

        "Hooked Demon": {
            "Size": "Normal",
            "Level": 4,
            "Monster Role": "Mook",
            "Type": "Demon",
            "IB": 12,
            "Attack": {
                "Hooks and barbs +14 vs. AC": "27 damage.\nNatural 16+: The hooked demon can make another hooks and barbs attack as a free action (and yes, this can keep going up to a maximum number of attacks equal to the escalation die + 1).",
                "Nastier Specials\nBleeding wounds": "Whenever the hooked demon hits a creature with hooks and barbs, that creature takes 10 damage each time it makes a non-basic attack (save ends)."
            },
            "AC": 23,
            "PD": 21,
            "MD": 17,
            "HP": 45
        },

        "Derro Sage": {
            "Size": "Normal",
            "Level": 4,
            "Monster Role": "Caster",
            "Type": "Humanoid",
            "IB": 7,
            "Attack": {
                "Staff +7 vs. AC": "7 damage.\nNatural 16+: The derro can cast one of the following close- quarters spells as a quick action this turn.\nCloaking dark: All nearby derro gain a +1 bonus to attacks and defenses until end of the derro sage’s next turn (cumulative).\nSonic squeal: Two random nearby non-derro creatures take 2d8 thunder damage.",
                "R: Mind scream +9 vs. MD": "12 psychic damage, and the target is confused (make a basic or at- will attack vs. ally) until the end of the derro sage’s next turn.\nNatural 16+: The derro sage can make another mind scream attack against a different nearby target as a free action.",
                "Nastier Specials\nGroup gibbering": "The derro sage starts a group of derro gibbering as a quick action. It can maintain the gibber as a free action at the start of each turn by taking 1 damage. Each nearby non- derro creature that hears the gibber must roll a d6 at the start of its turn and takes psychic damage equal to the die roll or to the number of gibbering derro, whichever is lower."
            },
            "AC": 18,
            "PD": 15,
            "MD": 18,
            "HP": 40
        }
    },

    "DRAGON": {
        "Monster": False,

        "Random Dragon Abilities (d12)": {
            1: "True seeing — The dragon is immune to invisibility and ignores any illusions.",
            2: "Whipping tail — When an enemy engaged with the dragon rolls a natural 1 or 2 with an attack roll, the dragon can make an opportunity attack against that creature as a free action. The attack is set up by the dragon’s whipping tail but delivered by the dragon’s usual melee attack.",
            3: "Tough Hide — The dragon has a +1 bonus to AC.",
            4: "Twisted Mind — The dragon has a +2 bonus to MD.",
            5: "Nimble — The dragon has a +2 bonus to PD.",
            6: "No vulnerability—Unlike other dragons of its color, this dragon has no vulnerability. The PCs will figure that out the first time they try to use its supposed vulnerability against it. 7: Now I’m mad!—The first time the dragon is staggered each battle, it uses its breath weapon attack as a free action that does not count against the normal uses of its breath.",
            8: "Serious threat—Disengage checks against the dragon take a –5 penalty. When a creature fails to disengage from the dragon, it takes damage equal to double the dragon’s level.",
            9: "PC - style racial power—The dragon has one of the racial powers of a player character race. If the dragon’s story suggests a specific power, choose that. If you’d like the most common expression per color, here’s our take: white (halfling); black (halfling, half-orc, human, wood elf ); green (dwarf, dark elf ); blue (high elf, half-orc); red (half-orc, human, wood elf).",
            10: "Raw power—Until it is staggered, the dragon rolls 2d20 with its melee attacks and uses the higher roll.",
            11: "Damage aura — When an enemy starts its turn engaged with the dragon, it takes damage equal to the dragon’s level (adventurer tier), double the level (champion tier), or triple the level (epic tier). The damage type is the same as the dragon’s breath weapon.",
            12: "More breath — The dragon can use its intermittent breath 1d4 more times each battle. If its breath weapon isn’t intermittent (white and green dragons), the dragon gains the extra uses anyway, making it more dangerous than lesser specimens of its color.",
            13: "Humanoid form — The dragon is capable of shapechanging into a humanoid form, usually of a warrior or spellcaster appropriate to its nature and usually not obviously draconic, registering as a normal human or elf or whatever. This ability is best used for long-term dragon characters that make it worth the GM’s time to create a double- or triple-strength humanoid monster to represent the shapechanged form. The dragon has the PC-style racial power of their humanoid form, but only while in shapechanged form.",
            14: "Some Unique Thing — The dragon has an entirely unique characteristic, something akin to a player character’s one unique thing except that the dragon’s version may be relevant to combat. GM, if you don’t feel like making something up, choose an ability from the list above."
        },

        "Huge White Dragon": {
            "Size": "Huge",
            "Level": 5,
            "Monster Role": "Troop",
            "Type": "Dragon",
            "IB": 10,
            "Vulnerability": "Fire",
            "Attack": {
                "Claws and bite +9 vs. AC (2 attacks)": "25 damage.\nNatural 16+: The white dragon can make an ice breath attack as a free action.",
                "[Special trigger] C: Ice breath +9 vs. PD (1d3 nearby enemies)": "20 cold damage.\nNatural odd hit or miss: The dragon takes 2d8 damage.",
                "Resist cold 18+": "When a cold attack targets this creature, the attacker must roll a natural 18+ on the attack roll or it only deals half damage."
            },
            "AC": 21,
            "PD": 18,
            "MD": 14,
            "HP": 200
        },

        "Huge Red Dragon": {
            "Size": "Huge",
            "Level": 13,
            "Monster Role": "Wrecker",
            "Type": "Dragon",
            "IB": 19,
            "Attack": {
                "Fangs, claws, and tail +19 vs. AC (3 attacks)": "70 damage.\nFirst natural even hit or miss each turn: Roll a fourth fangs, claws, and tail attack.\nSecond natural even hit or miss each turn: Roll a fifth fangs, claws, and tail attack.",
                "C: Fiery breath+19 vs. PD (2d3 nearby or far away enemies)": "80 fire damage.\nMiss: Half damage.",
                "Intermittent breath": "A huge red dragon can use fiery breath 1d6 times per battle, but never two turns in a row.",
                "Fear": "While engaged with this creature, enemies with 144 hp or fewer are dazed (–4 attack) and do not add the escalation die to their attacks.",
                "Resist fire 18+": "When a fire attack targets this creature, the attacker must roll a natural 18+ on the attack roll or it only deals half damage."
            },
            "AC": 28,
            "PD": 27,
            "MD": 23,
            "HP": 1200
        }
    }
}