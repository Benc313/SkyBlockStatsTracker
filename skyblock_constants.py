SKILL_DATA = {
    "standard": [
        50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425,
        32425, 47425, 67425, 97425, 147425, 222425, 322425, 522425, 822425,
        1222425, 1722425, 2322425, 3022425, 3822425, 4722425, 5722425,
        6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425,
        17322425, 19222425, 21222425, 23322425, 25522425, 27822425,
        30222425, 32722425, 35322425, 38072425, 40972425, 44072425,
        47472425, 51172425, 55172425, 59472425, 64072425, 68972425,
        74172425, 79672425, 85472425, 91572425, 97972425, 104672425, 111672425
    ],
    "runecrafting": [
        50, 200, 450, 850, 1450, 2300, 3450, 4950, 6850, 9250, 12250, 
        15900, 20900, 27400, 35900, 46900, 61900, 81900, 106900, 136900, 
        176900, 226900, 286900, 356900, 446900
    ]
}
BESTIARY_THRESHOLDS = {
    "regular": [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000, 50000, 100000, 250000, 500000, 1000000],
    "fishing": [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000],
}

BESTIARY_FAMILIES = {
    "Private Island": {"bracket": "regular", "prefixes": {"Bat": ["bat"], "Creeper": ["creeper"], "Enderman": ["enderman"], "Skeleton": ["skeleton"], "Slime": ["slime"], "Spider": ["spider"], "Witch": ["witch"], "Zombie": ["zombie"]}},
    "Hub": {"bracket": "regular", "prefixes": {"Crypt Ghoul": ["crypt_ghoul"], "Golden Ghoul": ["golden_ghoul"], "Graveyard Zombie": ["graveyard_zombie"], "Old Wolf": ["old_wolf"], "Wolf": ["wolf"], "Zombie Villager": ["zombie_villager"]}},
    "The Farming Islands": {"bracket": "regular", "prefixes": {"Chicken": ["chicken"], "Cow": ["cow"], "Mushroom Cow": ["mushroom_cow"], "Pig": ["pig"], "Rabbit": ["rabbit"], "Sheep": ["sheep"]}},
    "Spider's Den": {"bracket": "regular", "prefixes": {"Arachne": ["arachne"], "Broodmother": ["broodmother"], "Dasher Spider": ["dasher_spider"], "Gravel Skeleton": ["gravel_skeleton"], "Rain Slime": ["rain_slime"], "Silverfish": ["silverfish"], "Spider Jockey": ["spider_jockey"], "Splitter Spider": ["splitter_spider"], "Voracious Spider": ["voracious_spider"], "Weaver Spider": ["weaver_spider"]}},
    "The End": {"bracket": "regular", "prefixes": {"Dragon": ["dragon"], "Enderman": ["enderman_"], "Endermite": ["endermite"], "Endstone Protector": ["endstone_protector"], "Obsidian Defender": ["obsidian_defender"], "Voidling": ["voidling"], "Watcher": ["watcher"], "Zealot": ["zealot"]}},
    "Crimson Isle": {"bracket": "regular", "prefixes": {"Ashfang": ["ashfang"], "Barbarian Duke X": ["barbarian_duke_x"], "Bladesoul": ["bladesoul"], "Blaze": ["blaze_"], "Flaming Spider": ["flaming_spider"], "Flare": ["flare"], "Ghast": ["ghast"], "Kada Knight": ["kada_knight"], "Mage Outlaw": ["mage_outlaw"], "Magma Boss": ["magma_boss"], "Magma Cube": ["magma_cube_"], "Matcho": ["matcho"], "Millennia-Aged Blaze": ["millennia_aged_blaze"], "Mushroom Bull": ["mushroom_bull"], "Smoldering Blaze": ["smoldering_blaze"], "Tentacle": ["tentacle"], "Vanquisher": ["vanquisher"], "Wither Skeleton": ["wither_skeleton"], "Wither Spectre": ["wither_spectre"]}},
    "Deep Caverns": {"bracket": "regular", "prefixes": {"Emerald Slime": ["emerald_slime"], "Lapis Zombie": ["lapis_zombie"], "Miner Skeleton": ["miner_skeleton"], "Miner Zombie": ["miner_zombie"], "Redstone Pigman": ["redstone_pigman"], "Sneaky Creeper": ["sneaky_creeper"]}},
    "Dwarven Mines": {"bracket": "regular", "prefixes": {"Diamond Goblin": ["diamond_goblin"], "Ghost": ["ghost"], "Glacite": ["glacite"], "Goblin": ["goblin"], "Golden Goblin": ["golden_goblin"], "Powder Ghast": ["powder_ghast"], "Star Sentry": ["star_sentry"], "Treasure Hoarder": ["treasure_hoarder"]}},
    "Crystal Hollows": {"bracket": "regular", "prefixes": {"Automaton": ["automaton"], "Bal": ["bal"], "Boss Corleone": ["boss_corleone"], "Butterfly": ["butterfly"], "Grunt": ["grunt"], "Key Guardian": ["key_guardian"], "Sludge": ["sludge"], "Thyst": ["thyst"], "Worm": ["worm"], "Yog": ["yog"]}},
    "The Park": {"bracket": "regular", "prefixes": {"Howling Spirit": ["howling_spirit"], "Pack Spirit": ["pack_spirit"], "Soul of the Alpha": ["soul_of_the_alpha"]}},
    "Spooky Festival": {"bracket": "regular", "prefixes": {"Crazy Witch": ["crazy_witch"], "Headless Horseman": ["headless_horseman"], "Phantom Spirit": ["phantom_spirit"], "Scary Jerry": ["scary_jerry"], "Trick or Treater": ["trick_or_treater"], "Wither Gourd": ["wither_gourd"], "Wraith": ["wraith"]}},
    "Mythological Creatures": {"bracket": "regular", "prefixes": {"Gaia Construct": ["gaia_construct"], "Minos Champion": ["minos_champion"], "Minos Hunter": ["minos_hunter"], "Minos Inquisitor": ["minos_inquisitor"], "Minotaur": ["minotaur"], "Siamese Lynx": ["siamese_lynx"]}},
    "Jerry": {"bracket": "regular", "prefixes": {"Jerry": ["blue_jerry", "golden_jerry", "green_jerry", "purple_jerry"]}},
    "Kuudra": {"bracket": "regular", "prefixes": {"Kuudra Mob": ["blazing_golem", "blight", "dropship", "explosive_imp", "inferno_magma_cube", "kuudra", "magma_follower", "wandering_blaze", "wither_sentry"]}},
    "Fishing": {"bracket": "fishing", "prefixes": {"Abyssal Miner": ["abyssal_miner"], "Agarimoo": ["agarimoo"], "Blue Ringed Octopus": ["blue_ringed_octopus"], "Carrot King": ["carrot_king"], "Catfish": ["catfish"], "Deep Sea Protector": ["deep_sea_protector"], "Frog Man": ["frog_man"], "Guardian Defender": ["guardian_defender"], "Mithril Grubber": ["mithril_grubber"], "Night Squid": ["night_squid"], "Oasis Mob": ["oasis_rabbit", "oasis_sheep"], "Poisoned Water Worm": ["poisoned_water_worm"], "Rider of the Deep": ["rider_of_the_deep"], "Sea Archer": ["sea_archer"], "Sea Guardian": ["sea_guardian"], "Sea Leech": ["sea_leech"], "Sea Walker": ["sea_walker"], "Sea Witch": ["sea_witch"], "Snapping Turtle": ["snapping_turtle"], "Squid": ["squid"], "The Sea Emperor": ["the_sea_emperor"], "Water Hydra": ["water_hydra"], "Water Worm": ["water_worm"], "Wiki Tiki": ["wiki_tiki"]}},
    "Lava Fishing": {"bracket": "fishing", "prefixes": {"Fiery Scuttler": ["fiery_scuttler"], "Fire Eel": ["fire_eel"], "Fireproof Witch": ["fireproof_witch"], "Flaming Worm": ["flaming_worm"], "Fried Chicken": ["fried_chicken"], "Lava Mob": ["lava_blaze", "lava_flame", "lava_leech", "lava_pigman"], "Lord Jawbus": ["lord_jawbus"], "Magma Slug": ["magma_slug"], "Moogma": ["moogma"], "Plhlegblast": ["plhlegblast"], "Pyroclastic Worm": ["pyroclastic_worm"], "Ragnarok": ["ragnarok"], "Taurus": ["taurus"], "Thunder": ["thunder"]}},
    "Spooky Festival Fishing": {"bracket": "fishing", "prefixes": {"Grim Reaper": ["grim_reaper"], "Nightmare": ["nightmare"], "Phantom Fisher": ["phantom_fisher"], "Scarecrow": ["scarecrow"], "Werewolf": ["werewolf"]}},
    "Fishing Festival": {"bracket": "fishing", "prefixes": {"Shark": ["blue_shark", "great_white_shark", "nurse_shark", "tiger_shark"]}},
    "Winter Fishing": {"bracket": "fishing", "prefixes": {"Frosty": ["frosty"], "Frozen Steve": ["frozen_steve"], "Grinch": ["grinch"], "Nutcracker": ["nutcracker"], "Reindrake": ["reindrake"], "Yeti": ["yeti"]}},
    "Backwater Bayou Fishing": {"bracket": "fishing", "prefixes": {"Alligator": ["alligator"], "Banshee": ["banshee"], "Bayou Sludge": ["bayou_sludge"], "Dumpster Diver": ["dumpster_diver"], "Titanoboa": ["titanoboa"], "Trash Gobbler": ["trash_gobbler"]}},
    "Catacombs": {"bracket": "regular", "prefixes": {"Angry Archaeologist": ["angry_archaeologist"], "Bat": ["dungeon_bat"], "Cellar Spider": ["cellar_spider"], "Lonely Spider": ["lonely_spider"], "Crypt Dreadlord": ["crypt_dreadlord"], "Crypt Lurker": ["crypt_lurker"], "Crypt Souleater": ["crypt_souleater"], "Fels": ["fels"], "Golem": ["golem"], "King Midas": ["king_midas"], "Lost Adventurer": ["lost_adventurer"], "Mimic": ["mimic"], "Scared Skeleton": ["scared_skeleton"], "Shadow Assassin": ["shadow_assassin"], "Dungeon Skeleton": ["skeleton_grunt", "skeleton_master", "skeleton_soldier", "skeletor"], "Sniper": ["sniper"], "Super Archer": ["super_archer"], "Super Tank Zombie": ["super_tank_zombie"], "Tank Zombie": ["tank_zombie"], "Terracotta": ["terracotta"], "Undead": ["undead"], "Undead Skeleton": ["undead_skeleton"], "Wither Guard": ["wither_guard"], "Wither Husk": ["wither_husk"], "Wither Miner": ["wither_miner"], "Withermancer": ["withermancer"], "Dungeon Zombie": ["zombie_commander", "zombie_grunt", "zombie_knight", "zombie_lord", "zombie_soldier"]}},
    "Garden": {"bracket": "regular", "prefixes": {"Beetle": ["beetle"], "Cricket": ["cricket"], "Earthworm": ["earthworm"], "Field Mouse": ["field_mouse"], "Fly": ["fly"], "Locust": ["locust"], "Mite": ["mite"], "Mosquito": ["mosquito"], "Moth": ["moth"], "Rat": ["rat"], "Slug": ["slug"]}}
}