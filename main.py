from agents import GameManager
from utils import Board, heuristic

def main():
    print("Game has started!")
    game = GameManager()
    game.start()

if __name__ == '__main__':
    main()