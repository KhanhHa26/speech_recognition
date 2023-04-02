class Player:
    def __init__(self, name, pokemon_party):
        """
        name: string
        pokemon_party: a list of Pokemon objects
        
        make an additional attribute called
        current_pokemon and set it to the first 
        pokemon in the list
        """
        self.name = name 
        self.pokemon_party = pokemon_party
        self.current_pokemon = pokemon_party[0]

      
    def list_pokemon(self): #worked 
        """
        Using a for loop, print the pokemon's name
        if the pokemon is fainted, add fainted
        if the pokemon is the current one 
        battling, add current
        """
        for pokemon in self.pokemon_party: 
          if pokemon is self.current_pokemon: 
            print(pokemon.name + ": Current")
          elif pokemon.is_alive() == True: 
            print(pokemon.name)
          else: 
            print(pokemon.name + ": Fainted")
            

    def get_pokemon(self, pokemon_name):
        """
        Use a for loop to search for and return a 
        pokemon from the list of pokemon that has the given pokemon_name
        
        pokemon_name: string
        
        if the pokemon does not exist, return 
        INVALID_POKEMON
        """
        for pokemon in self.pokemon_party: 
          if pokemon.name == pokemon_name: 
            return pokemon
        return "Invalid Pokemon"

        
    def switch(self, pokemon_name): #worked 
        """
        use self.get_pokemon() to get the pokemon with
        the given pokemon_name and set current_pokemon to
        that pokemon
        """
        new = self.get_pokemon(pokemon_name)
        
        if new == INVALID_POKEMON:
            return False

        if not new.is_alive():
            return False

        if new == self.current_pokemon:
            return False
            
        self.current_pokemon = new 

        return True
        
    def heal(self): #worked 
        """
        heal the current pokemon with the
        pokemon's heal method
        """

        self.current_pokemon.heal()

    def team_is_alive(self): #worked 
        """
        Using a for loop, search through the 
        list of pokemon and check if each
        pokemon are alive
        if any are alive, return true
        otherwise, return false
        """
        for pokemon in self.pokemon_party: 
          if pokemon.is_alive(): 
            return True 
        return False 

    def print_moves(self):  #worked 
        """
        Using a for loop, print the move for the current pokemon's list of moves
        """
        for pokemon in self.pokemon_party: 
          if pokemon is self.current_pokemon: 
            pokemon.print_moves()
            
    def attack(self, move_name, enemy_pokemon): #worked
        """
        Have the current pokemon attack the enemy pokemon
        using the attack method"""
        self.current_pokemon.attack(move_name, enemy_pokemon)


class Pokemon:
    def __init__(self, name, hp, moves, type, speed):
        """
        name, type: string
        hp, speed: int
        moves: list of Move objs

        make an additional attribute called max_hp
        and set it to the starting hp
        """
        self.name = name 
        self.hp = hp
        self.moves = moves 
        self.type = type 
        self.speed = speed
        self.max_hp = self.hp

    def is_alive(self): #worked 
        """
        Returns true if alive, false if fainted
        """
        if self.hp <= 0: 
          return False 
        else: 
          return True 
    
    def print_moves(self): #worked 
        """
        Use a for loop to print each move from the 
        list of moves
        """
        for move in self.moves: 
          print(move.name)

    def get_move(self, move_name):
        """
        Use a for loop to search for and return a 
        move from the list of moves that has the 
        given move_name
        
        move_name: string
        
        if the move does not exist, return 
        INVALID_MOVE
        """
        for move in self.moves:
          if move.name == move_name: 
            return move
        return INVALID_MOVE
          

    def take_damage(self, damage_amount): #worked
        """
        Decrease self's health by the damage_amount
        health cannot go below 0
        cast to int
        
        damage_amount: int/float
        """
        if self.hp - damage_amount < 0: 
          self.hp=0
        else: 
          self.hp -= damage_amount
          
        
    def attack(self, move_name, enemy):  #worked
        """
        to damage the enemy, you need to get the
        move and that move's multiplier against the
        enemy
        enemy should take damage from that move 
        (that is multipled by the multiplier)
        """
        move = self.get_move(move_name)
        multiplier = move.get_multiplier_against(enemy)
        damage = move.power * multiplier
        enemy.take_damage(damage)
      

    def heal(self): #worked 
        """
        increase health by 20
        cannot exceed max hp
        """
        if self.hp + 20 > self.max_hp: 
          self.hp = self.max_hp
        else: 
          self.hp += 20 


class Move:
    def __init__(self, name, power, type):
        self.name = name
        self.power = power
        self.type = type

    def __str__(self):
        return self.name + ": " + self.type + " type"

    def get_multiplier_against(self, pokemon):        
        if self.type == "grass":
            if pokemon.type == "water" or pokemon.type == "ground":
                return 2
            elif pokemon.type == "fire" or pokemon.type == "grass":
                return 0.5
            else:
                return 1
                
        elif self.type == "fire":
            if pokemon.type == "grass":
                return 2
            elif pokemon.type == "water" or pokemon.type == "fire":
                return 0.5
            else:
                return 1
                
        elif self.type == "water":
            if pokemon.type == "fire" or pokemon.type == "ground":
                return 2
            elif pokemon.type == "grass" or pokemon.type == "water":
                return 0.5
            else:
                return 1
                
        elif self.type == "ground": 
            if pokemon.type == "fire" or pokemon.type == "electric":
                return 2
            elif pokemon.type == "grass":
                return 0.5
            else:
                return 1
            
        elif self.type == "electric": 
            if pokemon.type == "water":
                return 2
            elif pokemon.type == "grass" or pokemon.type == "electric":
                return 0.5
            elif pokemon.type == "ground":
                return 0
            else:
                return 1
            
        else:
            return 1


INVALID_MOVE = Move("Invalid Move", 0, 'no type')
INVALID_POKEMON = Pokemon("MissingNo.", 1, [INVALID_MOVE], 'no type', 0)
