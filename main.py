from dino import run_game_cycle
from neuro import run_neuro_cycle
import time

if __name__ == '__main__':
    time.sleep(0.1)
    run_neuro_cycle()
    run_game_cycle()
