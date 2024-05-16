from Agents.GameAgents import RandomPlayer
from GameEnviroment.GamePlay import play

def main():
    # Defining the players
    player1 = RandomPlayer("Harol")
    player2 = RandomPlayer("Raul")

    # initializing the game
    play(player1, player2)

if __name__ == '__main__':
    main()
