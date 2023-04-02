from .pokemon import Pokemon, Move


def create_team():
    """
    Build a list of Pokemon in this function, and return the list.
    
    The team that you build here will be used as your team in the Pokemon
    tournament.

    """
    
    #ground move
    earth_power = Move("Earth Power", 90, "ground")
    mud_shot = Move("Mud Shot", 55, "ground")
    rock_tomb = Move("Rock Tomb", 60, "ground")
    rock_smash = Move("Rock Smash", 40, "ground")
    
    #fire move
    ember = Move("Ember", 40, "fire")
    flamethrower = Move("Flamethrower", 90, "fire")
    fire_spin = Move("Fire Spin", 35, "fire")
    fire_fang = Move("Fire Fang", 65, "fire")
    flame_wheel = Move("Flame Wheel", 60, "fire")
    
    #grass move
    seed_bomb = Move("Seed Bomb", 80, "grass")
    vine_whip = Move("Vine Whip", 45, "grass")
    bullet_seed = Move("Bullet Seed", 25, "grass")
    razor_leaf = Move("Razor Leaf", 55, "grass")
    
    #electric move
    thunder_shock = Move("Thunder Shock", 40, "electric")
    thunderbolt = Move("Thunderbolt", 90, "electric")
    electro_ball = Move("Electro ball", 40, "electric")
    spark = Move("Spark", 65, "electric")
    charge_beam = Move("Charge Beam", 50, "electric")
    
    #water move
    water_gun = Move("Water Gun", 40, "water")
    aqua_tail = Move("Aqua Tail", 90, "water")
    brine = Move("Brine", 65, "water")
    water_pulse = Move("Water Pulse", 60, "water")
    whirlpool = Move("Whirlpool", 35, "water")
    
    # pokemons
    Infernape = Pokemon("Infernape", 183, [ember, flame_wheel, fire_spin, fire_fang], "fire", 105)
    Bulbasaur = Pokemon("Bulbasaur", 152, [razor_leaf, seed_bomb, vine_whip, bullet_seed], "grass", 45)
    Piplup = Pokemon("Piplup", 160, [water_gun, water_pulse, aqua_tail, brine], "water", 40)
    Mareep = Pokemon("Mareep", 162, [thunder_shock, thunderbolt, charge_beam, spark], "electric", 65)
    
    Pikachu = Pokemon("Pikachu", 142, [thunder_shock, thunderbolt, electro_ball, spark], "electric", 90)
    Squirtle = Pokemon("Squirtle", 151, [water_gun, aqua_tail, brine, whirlpool], "water", 43)
    Charmander = Pokemon("Charmander", 146, [ember, flamethrower, fire_spin, fire_fang], "fire", 65)
    Groudon = Pokemon("Groudon", 170, [earth_power, mud_shot, rock_tomb, rock_smash], "ground", 90)
    
    return [Pikachu, Squirtle, Charmander, Groudon]

