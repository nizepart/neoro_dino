import threading

from dino import invoke_jump_event


def run_neuro_cycle():
    invoke_jump_event()
    threading.Timer(0.1, run_neuro_cycle).start()


run_neuro_cycle()
