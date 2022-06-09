import threading
from pyfirmata import Arduino, util
from dino import invoke_jump_event

board = Arduino('COM7')

it = util.Iterator(board)
it.start()
# board.analog[0].enable_reporting()

analog_0 = board.get_pin('a:0:i')


def run_neuro_cycle():
    value = float(analog_0.read())
    if value > 0.8:
        invoke_jump_event()
    print(value)
    threading.Timer(0.01, run_neuro_cycle).start()