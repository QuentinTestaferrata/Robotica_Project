#Code Written by Quentin Testaferrata
#EhB 2e Bachelor TI

import os
import sys
import time
import math
import keyboard

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)

arm = XArmAPI(ip)
arm.motion_enable(enable = True)
arm.set_mode(0)
arm.set_state(state=0)

arm.reset(wait = True)

speed = 50
#initiele posities
x_pos = 206
y_pos = 0
z_pos = 120.5
#ZQSDAE bewegingen op de X, Y en Z-as
movement_speed = 15

#predefinieerde posities
positions = [
    [206, 355, 60, 180, 0, 0], #links arrow
    [500, 0, 240, 180, 0, 0],  #up arrow
    [206, -355, 60, 180, 0, 0] #rechts arrow
]
#Voor de loop
angles = {
    'bovenbordPositie':[256, -13, 120, 180, 0, 0],
    'opBordPositie':[256, -13, 10.8, 180, 0, 0],
    'bovenbordPos':[256, -13, 60, 180, 0, 0],
    'tussenPositie':[256, -344, 60, 180, 0, 0],
    'neerleggen':[260, -375, 15, 180, 0, 0],
    'trekken':[260, -375, 40, 180, 0, 0],
}

#De positie van arm updaten (Zonder parameters)
def update_positie():
    global x_pos, y_pos, z_pos
    arm.set_position(x = x_pos, y = y_pos, z = z_pos, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
    print(f"xArm position: X = {x_pos}, Y = {y_pos}, Z = {z_pos}")
#De positie van arm updaten (Met parameters)
def update_positie_met_param(x, y, z):
    arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
    print(f"xArm position: X = {x}, Y = {y}, Z = {z}")

print("Z om naar voor te gaan op X-as, S naar achter") #Done
print("Q om naar voor te gaan op Y-as, D naar achter") #Done
print("A om naar voor te gaan op Z-as, E naar achter") #Done
print("Druk op Spacebar om de arm op default locatie te zetten") #Done
print("Druk op Escape om het script te stoppen") #Done
print("Druk op L voor een Loop example, M ingedrukt houden om te stoppen") #Done
print("Pijlen Up, Left, Right voor Predefined posities")

try: 
    looping = False

    while True:
        #ZQSDAE moving
        if keyboard.is_pressed('z'):
            while keyboard.is_pressed('z'):
                x_pos += movement_speed
                update_positie()
                time.sleep(0)
        if keyboard.is_pressed('s'):
            while keyboard.is_pressed('s'):
                x_pos -= movement_speed
                update_positie()
                time.sleep(0)
        if keyboard.is_pressed('q'):
            while keyboard.is_pressed('q'):
                y_pos += movement_speed
                update_positie()
                time.sleep(0)
        if keyboard.is_pressed('d'):
            while keyboard.is_pressed('d'):
                y_pos -= movement_speed
                update_positie()
                time.sleep(0)
        if keyboard.is_pressed('a'):
            while keyboard.is_pressed('a'):
                z_pos += movement_speed
                update_positie()
                time.sleep(0)
        if keyboard.is_pressed('e'):
            while keyboard.is_pressed('e'):
                z_pos -= movement_speed
                update_positie()
                time.sleep(0)

        #Loop
        if keyboard.is_pressed('l') and not looping:
            looping = True
            print("Loop started")
        elif keyboard.is_pressed('m') and looping:
            looping = False
            print("Loop stopped")
        elif looping:
            for position_name, position in angles.items():
                x_pos, y_pos, z_pos, _, _, _ = position
                update_positie_met_param(x_pos, y_pos, z_pos)
                time.sleep(1)

        #Predefined positions
        if keyboard.is_pressed('up'):
            x_pos, y_pos, z_pos, _, _, _ = positions[1]
            update_positie()
        if keyboard.is_pressed('left'):
            x_pos, y_pos, z_pos, _, _, _ = positions[0]
            update_positie()
        if keyboard.is_pressed('right'):
            x_pos, y_pos, z_pos, _, _, _ = positions[2]
            update_positie()

        #default pos
        if keyboard.is_pressed('space'):
            arm.reset(wait=True)
            x_pos = 206
            y_pos = 0
            z_pos = 120.5
            update_positie()
            arm.reset(wait=True)
        
        #exit
        if keyboard.is_pressed('esc'):
            arm.reset(wait=True)
            arm.disconnect()
            exit()

except KeyboardInterrupt:
    arm.reset(wait=False)
    arm.disconnect()
