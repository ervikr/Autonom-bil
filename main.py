import signal
import serial_arduino
import time
from xbox360controller import Xbox360Controller

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def on_button_pressed(button):
    serial_arduino.send_data("btnA")
    print('Button {0} was pressed'.format(button.name))
    time.sleep(0.02)


def on_axis_l_moved(axis):
    serial_arduino.send_data("jlx" + str(round(axis.x, 2)))
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    time.sleep(0.02)
    
def on_axis_r_moved(axis):
    serial_arduino.send_data("rt" + str(int(map_range(axis.y, -1, 1, 0, 255))))
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    time.sleep(0.02)

with Xbox360Controller(0, axis_threshold=0.2) as controller:
        # Button A events
        controller.button_a.when_pressed = on_button_pressed
        # Left and right axis move event
        controller.axis_l.when_moved = on_axis_l_moved
        controller.axis_r.when_moved = on_axis_r_moved
        signal.pause()