import asyncio
from evdev import InputDevice, ecodes, ff, list_devices

class Controller():
    def __init__(self, dev = '/dev/input/event3') -> None:
        self.power_on = True
        self.device = InputDevice(dev)
        self.joystick_left_y_flag = False
        self.joystick_left_x_flag = False
        self.joystick_right_y_flag = False
        self.joystick_right_x_flag = False
        self.joystick_left_y = 0 # values are mapped to [-1 ... 1]
        self.joystick_left_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_y = 0 # values are mapped to [-1 ... 1]
        self.trigger_right = 0 # values are mapped to [0 ... 1]
        self.trigger_left = 0 # values are mapped to [0 ... 1]
        self.button_x = False
        self.button_y = False
        self.button_b = False
        self.button_a = False
        self.dpad_up = False
        self.dpad_down = False
        self.dpad_left = False
        self.dpad_right = False
        self.bumper_left = False
        self.bumper_right = False
        self.button_menu = False
        self.button_view = False
        self.rumble_effect = 0
        self.effect1_id = 0 # light rumble, played continuously
        self.effect2_id = 0 # strong rumble, played once
    
    async def read_controller_input(self):
        max_abs_joystick_left_x = 0xFFFF/2
        uncertainty_joystick_left_x = 2500
        max_abs_joystick_left_y = 0xFFFF/2
        uncertainty_joystick_left_y = 2500
        max_abs_joystick_right_x = 0xFFFF/2
        uncertainty_joystick_right_x = 2000
        max_abs_joystick_right_y = 0xFFFF/2
        uncertainty_joystick_right_y = 2000
        max_trigger = 1023

        async for event in self.device.async_read_loop():
            if not(self.power_on): #stop reading device when power_on = false
                    break
            
            if event.type == 3:
                if event.code == 1: # left joystick y-axis
                    self.joystick_left_y_flag = True
                    if -event.value > uncertainty_joystick_left_y:
                        self.joystick_left_y = (-event.value - uncertainty_joystick_left_y) / (max_abs_joystick_left_y - uncertainty_joystick_left_y + 1)
                    elif -event.value < -uncertainty_joystick_left_y:
                        self.joystick_left_y = (-event.value + uncertainty_joystick_left_y) / (max_abs_joystick_left_y - uncertainty_joystick_left_y + 1)
                    else:
                        self.joystick_left_y = 0
                elif event.code == 0: # left joystick x-axis
                    self.joystick_left_x_flag = True
                    if event.value > uncertainty_joystick_left_x:
                        self.joystick_left_x = (event.value - uncertainty_joystick_left_x) / (max_abs_joystick_left_x - uncertainty_joystick_left_x + 1)
                    elif event.value < -uncertainty_joystick_left_x:
                        self.joystick_left_x = (event.value + uncertainty_joystick_left_x) / (max_abs_joystick_left_x - uncertainty_joystick_left_x + 1)
                    else:
                        self.joystick_left_x = 0
                elif event.code == 3: # right joystick x-axis
                    self.joystick_right_x_flag = True
                    if event.value > uncertainty_joystick_right_x:
                        self.joystick_right_x = (event.value - uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                    elif event.value < -uncertainty_joystick_right_x:
                        self.joystick_right_x = (event.value + uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                    else:
                        self.joystick_right_x = 0
                elif event.code == 4: # right joystick y-axis
                    self.joystick_right_y_flag = True
                    if -event.value > uncertainty_joystick_right_y:
                        self.joystick_right_y = (-event.value - uncertainty_joystick_right_y) / (max_abs_joystick_right_y - uncertainty_joystick_right_y + 1)
                    elif -event.value < -uncertainty_joystick_right_y:
                        self.joystick_right_y = (-event.value + uncertainty_joystick_right_y) / (max_abs_joystick_right_y - uncertainty_joystick_right_y + 1)
                    else:
                        self.joystick_right_y = 0
                elif event.code == 5: # right trigger
                    self.trigger_right = event.value / max_trigger
                elif event.code == 2: # left trigger
                    self.trigger_left = event.value / max_trigger
                elif event.code == 16: # dpad left/right
                    self.dpad = True
                    self.dpad_left_right = event.value
                elif event.code == 17: # dpad up/down
                    self.dpad = True
                    self.dpad_up_down = event.value


            if event.type == 1:
                match event.code:
                    case 304:
                        self.button_a = True
                        print("Button A pressed")
                    case 305:
                        self.button_b = True
                    case 306:
                        self.button_x = True
                    case 307:
                        self.button_y = True
                    case 308:
                        self.bumper_left = True
                    case 309:
                        self.bumper_right = True
                    case 310:
                        self.button_menu = True
                    case 311:
                        self.button_view = True
                     
    
    async def rumble(self): # asyncronus control of force feed back effects
        repeat_count = 1
        while self.power_on:
            if self.rumble_effect == 1:
                self.device.write(ecodes.EV_FF, self.effect1_id, repeat_count)
            elif self.rumble_effect == 2:
                self.device.write(ecodes.EV_FF, self.effect2_id, repeat_count)
                self.rumble_effect = 0 # turn of effect in order to play effect2 only once
            await asyncio.sleep(0.2)

    def erase_rumble(self):
        self.device.erase_effect(self.effect1_id)

if __name__ == '__main__':
            
    async def main():
        controller = Controller(dev = '/dev/input/event7')
        await controller.read_controller_input()
        print("yes")
        if controller.button_a:
            print("Button AAAA Pressed")
            
    asyncio.run(main())