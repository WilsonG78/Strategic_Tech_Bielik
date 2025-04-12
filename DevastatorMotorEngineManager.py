#!/usr/bin/python3

from typing import List
import RPi.GPIO as gpio
import sys, termios, tty, os, time

class DevastatorMotorEngineManager:
    """The DevastatorMotorEngineManager class manages the engines of the devastator robot.
    This is achieved by interfacing with the L298N motor driver via GPIO pins on a Raspberry Pi using the RPi.GPIO library."""

    pins: List[int]
    direction_forward: bool = True
    pwm_controler1: gpio.PWM
    pwm_controler2: gpio.PWM
    pwm_power: int

    def __init__(self, pins: List[int] = [25, 17, 22, 23, 24, 27]):
        """Initializes the motor controller by setting up GPIO pins.
        Pin 25 is used for the enable signal, and the physical pins mapped to GPIO are [22, 11, 15, 16, 18, 13]."""
        self.pins = pins
        gpio.setmode(gpio.BCM)
        for i in pins:
            gpio.setup(i, gpio.OUT)
        for i in pins:
            gpio.output(i, gpio.LOW)
        self.pwm_power = 100
        self.pwm_controler = gpio.PWM(pins[0], self.pwm_power)
        self.pwm_controler.start(0)
    def __del__(self):
        '''We stop the motor'''
        for i in self.pins:
            gpio.output(i, gpio.LOW)
        gpio.cleanup()
    def turn_right(self,keyboard_interupt: str) -> None:
        '''We turn the motor to the right'''
        if keyboard_interupt == 'd':
            gpio.output(self.pins[1], gpio.LOW)
            gpio.output(self.pins[2], gpio.HIGH)
            gpio.output(self.pins[3], gpio.LOW)
            gpio.output(self.pins[4], gpio.LOW)
        return
    def turn_left(self,keyboard_interupt: str) -> None:
        '''We turn the motor to the left'''
        if keyboard_interupt == 'a':
            gpio.output(self.pins[1], gpio.HIGH)
            gpio.output(self.pins[2], gpio.LOW)
            gpio.output(self.pins[3], gpio.HIGH)
            gpio.output(self.pins[4], gpio.LOW)
    def go_forward(self,keyboard_interupt: str) -> None:
        '''We turn the motor forward'''
        if keyboard_interupt == 'w':
            self.direction_forward = True
            gpio.output(self.pins[1], gpio.HIGH)
            gpio.output(self.pins[2], gpio.HIGH)
            gpio.output(self.pins[3], gpio.LOW)
            gpio.output(self.pins[4], gpio.LOW)
    def go_back(self,keyboard_interupt: str) -> None:
        '''We turn the motor backward'''
        if keyboard_interupt == 's':
            self.direction_forward = False
            gpio.output(self.pins[1], gpio.LOW)
            gpio.output(self.pins[2], gpio.HIGH)
            gpio.output(self.pins[3], gpio.LOW)
            gpio.output(self.pins[4], gpio.HIGH)
    def power_control(self,keyboard_interupt: str) ->None:
        '''We control the power of the motor'''
        if keyboard_interupt == 'u' and self.pwm_power < 900:
            self.pwm_power += 100
            self.pwm_controler.ChangeDutyCycle(self.pwm_power)
        elif keyboard_interupt == 'i' and self.pwm_power > 900:
            self.pwm_power -= 100
            self.pwm_controler.ChangeDutyCycle(self.pwm_power)
    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def working(self):
        button_delay = 0.1
        while True:
            char = self.getch()
            self.turn_right(char)
            self.turn_left(char)
            self.go_forward(char)
            self.go_back(char)
            self.power_control(char)
            if char == 'e':
                self.__del__()
            gpio.output(self.pins[0],gpio.LOW)
            time.sleep(button_delay)
