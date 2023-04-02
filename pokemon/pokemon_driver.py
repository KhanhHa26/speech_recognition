
import random

from pokemon import Player, Pokemon, Move, INVALID_MOVE, INVALID_POKEMON


class Action:
    """Base class representing an action that a player can take during
    their turn.
    """

    def __init__(self, player, priority):
        self.player = player

        # Priority used for the purposes of .should_perform_before().
        # Higher-priority Actions will go first.
        self.priority = priority

    def should_perform_before(self, otherAction):
        '''Returns True if this Action should be performed before another
        Action, or False otherwise.
        '''
        return self.priority > otherAction.priority

    def perform_action(self):
        '''Executes this Action. Subclasses must implement this.'''
        raise NotImplementedError


class AttackAction(Action):
    """An Action that represents a player's Pokemon attacking another."""

    def __init__(self, player, moveName, opponent):
        super().__init__(player, 0)
        self.moveName = moveName
        self.opponent = opponent

    def should_perform_before(self, otherAction):
        # If the other action is an AttackAction, we go first if our
        # Pokemon's speed is greater than the other Pokemon's speed.
        if isinstance(otherAction, AttackAction):
            mySpeed = self.player.current_pokemon.speed
            otherSpeed = otherAction.player.current_pokemon.speed

            if mySpeed > otherSpeed:
                return True
            elif mySpeed < otherSpeed:
                return False
            else:
                return random.randint(0, 1) == 0

        # Otherwise, just use normal priority rules.
        else:
            return super().should_perform_before(otherAction)

    def perform_action(self):
        move = self.player.current_pokemon.get_move(self.moveName)
        print(f"{self.player.current_pokemon.name} used {move.name}!")

        targetPokemon = self.opponent.current_pokemon

        multiplier = move.get_multiplier_against(targetPokemon)
        if multiplier > 1:
            print("It's super effective!")
        elif multiplier == 0:
            print(f"It doesn't affect {targetPokemon.name}...")
        elif multiplier < 1:
            print("It's not very effective...")

        self.player.attack(self.moveName, targetPokemon)


class SwitchAction(Action):
    """An Action that represents a player switching their Pokemon for another."""

    def __init__(self, player, pokemonName):
        super().__init__(player, 1)
        self.pokemonName = pokemonName

    def perform_action(self):
        if self.player.current_pokemon.is_alive():
            print(f"{self.player.current_pokemon.name}, return!")

        self.player.switch(self.pokemonName)

        pokemon = self.player.get_pokemon(self.pokemonName)
        print(f"Go {pokemon.name}!")


class HealAction(Action):
    """An Action that represents a player healing their Pokemon."""

    def __init__(self, player):
        super().__init__(player, 2)

    def perform_action(self):
        print(f"{self.player.name} used a potion on {self.player.current_pokemon.name}!")
        self.player.heal()


class RunAction(Action):
    """An Action that represents a player running away."""

    def __init__(self, player):
        super().__init__(player, 3)

    def perform_action(self):
        print(f"{self.player.name} ran away!")


class TurnResult:
    """Represents the result of performing both players' Actions in a single
    turn. The result will either be a Game Over or *not* a Game Over, possibly
    with a winner and loser.
    """

    def __init__(self, gameOver=False, winner=None, loser=None):
        self.gameOver = gameOver
        self.winner = winner
        self.loser = loser


def handle_attack(player, opponent):
    """Asks the given player to choose an attacking move against the given
    opponent player.

    Returns an AttackAction representing the selected attack.
    """

    print(f"\n{player.current_pokemon.name}'s Moves:")
    player.print_moves()

    print()

    while True:
        moveName = input("Choose a move: ")
        move = player.current_pokemon.get_move(moveName)
        if move is INVALID_MOVE:
            print(f"{player.current_pokemon.name} doesn't know {moveName}!")
        else:
            return AttackAction(player, moveName, opponent)


def handle_switch(player):
    """Asks the given player to choose a Pokemon to switch to.

    Returns a SwitchAction representing the action of switching to the selected
    Pokemon.
    """

    print(f"\n{player.name} should switch to which pokemon?")
    player.list_pokemon()

    print()

    while True:
        pokemonName = input("Choose a Pokemon: ")
        pokemon = player.get_pokemon(pokemonName)
        if pokemon is INVALID_POKEMON:
            print("Invalid pokemon!")
        elif not pokemon.is_alive():
            print(f"{pokemon.name} can't battle!")
        elif pokemon is player.current_pokemon:
            print(f"{pokemon.name} is already out!")
        else:
            return SwitchAction(player, pokemonName)


def choose_action(player, opponent):
    """Asks the given player (facing off against the given opponent player) to
    choose an action to perform for the current turn.

    Returns an Action object representing the action that the player chose to do
    for the current turn.
    """

    print(f"{player.name}'s turn.")
    print()
    print("Commands:")
    print("attack / switch / heal / run")
    print()

    while True:
        command = input(f"What will {player.name} do? ").lower()

        if command == 'attack':
            return handle_attack(player, opponent)

        elif command == 'switch':
            return handle_switch(player)

        elif command == 'heal':
            return HealAction(player)

        elif command == 'run':
            return RunAction(player)

        else:
            print(":(")


def handle_fainting(player):
    """Takes a plaier, and determines whether that player's currently-active
    Pokemon has fainted.

    If the player's currently-active Pokemon has fainted, asks that player
    which Pokemon they would like to switch to, if any are available, and
    immediately executes the switch.

    Returns True if the player's currently-active Pokemon has fainted, and
    False otherwise.
    """

    if not player.current_pokemon.is_alive():
        print(f"{player.current_pokemon.name} fainted!")
        if player.team_is_alive():
            handle_switch(player).perform_action()

        return True

    else:
        return False


def execute_turn(p1Action, p2Action):
    """Takes two Action objects and executes a single battle turn using
    those actions. The Action that is performed first is determined by the
    result of Action.should_perform_before().

    If a Pokemon faints as a result of the first Action that executes during this
    turn, that Pokemon will not perform its own Action.

    Returns a TurnResult object representing the result of executing this turn.
    If the game should not continue, the TurnResult will have its .gameOver
    attribute set to True.
    """

    player1 = p1Action.player
    player2 = p2Action.player


    #####################
    # Running Away Case #
    #####################

    player1Ran = isinstance(p1Action, RunAction)
    player2Ran = isinstance(p2Action, RunAction)

    # Handle all the weird combinations of cases where players are running away.
    if player1Ran:
        p1Action.perform_action()

        if player2Ran:
            p2Action.perform_action()

            # If both players ran, then there is no winner.
            return TurnResult(gameOver=True)

        else:
            # If only Player 1 ran, then Player 2 is the winner.
            return TurnResult(gameOver=True, winner=player2, loser=player1)

    elif player2Ran:
        p2Action.perform_action()

        if player1Ran:
            p1Action.perform_action()

            # If both players ran, then there is no winner.
            return TurnResult(gameOver=True)

        else:
            # If only Player 2 ran, then Player 1 is the winner.
            return TurnResult(gameOver=True, winner=player1, loser=player2)


    #########################
    # Not-Running-Away Case #
    #########################

    # In what order should we perform these actions?
    if p1Action.should_perform_before(p2Action):
        # Player 1's Action goes first.
        p1Action.perform_action()
        fainted = handle_fainting(player2)

        # Only perform Player 2's Action if Player 1's Action
        # didn't result in Player 2's Pokemon fainting.
        if not fainted:
            p2Action.perform_action()
            fainted = handle_fainting(player1)

    else:
        # Player 2's Action goes first.
        p2Action.perform_action()
        fainted = handle_fainting(player1)

        # Only perform Player 1's Action if Player 2's Action
        # didn't result in Player 1's Pokemon fainting.
        if not fainted:
            p1Action.perform_action()
            fainted = handle_fainting(player2)

    # If either Pokemon fainted, check to see if the game is over.
    if fainted:
        player1HasPokemon = player1.team_is_alive()
        player2HasPokemon = player2.team_is_alive()

        if player1HasPokemon and not player2HasPokemon:
            # Only Player 1 has any Pokemon left. Player 1 wins!
            return TurnResult(
                gameOver=True,
                winner=player1,
                loser=player2,
            )
        elif not player1HasPokemon and player2HasPokemon:
            # Only Player 2 has any Pokemon left. Player 2 wins!
            return TurnResult(
                gameOver=True,
                winner=player2,
                loser=player1,
            )
        elif not player1HasPokemon and not player2HasPokemon:
            # ... somehow neither player has any Pokemon left?
            # How did this happen??? O.o
            return TurnResult(gameOver=True)

    # Both players still have at least Pokemon left. Continue battling!
    return TurnResult(gameOver=False)


def main(player1, player2):
    """The main battle driver loop. Takes two valid Player objects representing
    the two contestants of this battle.
    """

    while True:
        print(f"{player1.name}'s Pokemon: {player1.current_pokemon.name}")
        print(f"{player1.current_pokemon.hp} HP")
        print()
        print(f"{player2.name}'s Pokemon: {player2.current_pokemon.name}")
        print(f"{player2.current_pokemon.hp} HP")
        print()

        p1Action = choose_action(player1, player2)
        print()

        p2Action = choose_action(player2, player1)
        print()

        print("======================================================\n")

        result = execute_turn(p1Action, p2Action)

        print()
        print("======================================================\n")

        if result.gameOver:
            if result.loser is not None:
                print(f"{result.loser.name} loses!")

            if result.winner is not None:
                print(f"{result.winner.name} is the winner!")

            break

    print("Game over.")
