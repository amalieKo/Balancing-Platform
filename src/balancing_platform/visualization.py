# Importing packages
from vpython import *
import numpy as np
from simple_pid import PID

pid_x = PID(2, 0.1, 0.05, setpoint=0)
pid_z = PID(1, 0.1, 0.05, setpoint=0)

# Creating simulation scene
scene.title = "Balancing Platform Visualization"
scene.x = 0
scene.y = 0
scene.width = 800
scene.height = 600
scene.range = 30
scene.center = vector(1, 0, 0)
scene.background = vector(0, 0, 0)

# Specify colors - Funker ikke...
# c = (229, 255, 204)
# c2 = color.rgb_to_hsv(c)  # convert RGB to HSV

# Creating objects
ball = sphere(pos=vector(0, 0.745, 0), radius=0.5,  make_trail=True, color=color.yellow)
platform = box(pos=vector(0, 0, 0), size=vector(50, 0.5, 50), color=color.red)
floor = box(pos=vector(0, -8.75, 0), size=vector(100, 1, 100), color=color.cyan)
# wall_1 = box(pos=vector(50, 40, 0), size=vector(5, 100, 100), color=color.blue)
# wall_2 = box(pos=vector(-50, 40, 0), size=vector(5, 100, 100), color=color.blue)
# wall_3 = box(pos=vector(0, 40, -50), size=vector(100, 100, 5), color=color.blue)
leg_3 = cylinder(pos=vector(20, -8.75, 20), axis=vector(0, 8.75, 0), radius=1, color=color.green)
leg_2 = cylinder(pos=vector(-20, -8.75, 20), axis=vector(0, 8.75, 0), radius=1, color=color.blue)
leg_1 = cylinder(pos=vector(0, -8.75, -20), axis=vector(0, 8.75, 0), radius=1, color=color.purple)


def update_x(power, dt):
        ball.pos.x += 1 * power * dt


def update_z(power, dt):
        ball.pos.z += 1 * power * dt


def ellipse():
    pid_x.setpoint = 2 + 20 * cos(t)
    pid_z.setpoint = 1 + 12.5 * sin(t)


def circle():
    pid_x.setpoint = 2 + 25 * cos(t)
    pid_z.setpoint = 2 + 25 * sin(t)


def number_8():
    pid_x.setpoint = 2 + (25 * cos(t)) / (1 + sin(t) * sin(t))
    pid_z.setpoint = 1 + (25 * sin(t) * cos(t)) / (1 + sin(t) * sin(t))


dt = 0.01  # Hvor fort cylinderne øker
t = 0

xValue = 0
yValue = 0
length = 50.0  # 45.00||
Z0 = 8.75  # 9.00
offset = 4.0

'''
# Simulation
while True:
    rate(100)
    number_8()
    control_x = pid_x(ball.pos.x)
    control_z = pid_z(ball.pos.z)
    update_x(control_x, dt)
    update_z(control_z, dt)
    t += dt

'''

leg1_running = True
leg2_running = True
leg3_running = True

running = True
maxHeight = 13.00

while running:
    rate(100)
    roll = xValue * (pi / 180.0)
    pitch = yValue * (pi / 180.0)

    if leg1_running:
        heightM1 = (sqrt(3) / 3) * length * pitch + Z0
        leg_1.axis.y = heightM1

    if leg2_running:
        heightM2 = -(sqrt(3) / 6) * length * pitch + (length / 2) * roll + Z0
        leg_2.axis.y = heightM2

    if leg3_running:
        heightM3 = -(sqrt(3) / 6) * length * pitch + (length / 2) * roll + Z0
        leg_3.axis.y = heightM3

    yValue += dt
    xValue += dt

    platform.pos.y = (heightM1 - 8.75)  # (0, y, 0) endrer seg etter heightM1
    ball.pos.y = (platform.pos.y + 0.745)

    print('Height: ', heightM1, '   ', heightM2, '   ', heightM3, '          ', platform.pos)

    if heightM1 > maxHeight:
        leg1_running = False

    if heightM2 > maxHeight:
        leg2_running = False

    if heightM3 > maxHeight:
        leg3_running = False

    if (heightM1 and heightM2 and heightM3) > maxHeight:
        running = False
        print("Visualization stopped")
