#!/usr/bin/python3

from typing import List
import RPi.GPIO as gpio
import sys, termios, tty, os, time
import readchar


class DevastatorMotorEngineManager:
    """Engine Manager is to manage the engines of the devastator
    we communicate to L298N through GPIO pins on the raspberry pi
    we use RPi.GPIO library to do so."""

    pins: List[int]
    direction_forward: bool = True
    pwm_controler: gpio.PWM
    pwm_power: int

    def __init__(self, pins: List[int] = [25, 17, 22, 23, 24, 27]):
        """We set up the pins en pin is 25 GPIO physical pins are [22,11,15,16,18,13]"""
        self.pins = pins
        gpio.setmode(gpio.BCM)
        for i in pins:
            gpio.setup(i, gpio.OUT)
        for i in pins:
            gpio.output(i, gpio.LOW)
        self.pwm_power = 1000
        self.pwm_controler1 = gpio.PWM(pins[0], self.pwm_power)
        self.pwm_controler2 = gpio.PWM(pins[5], self.pwm_power)
        self.pwm_controler.start(100)

    def turn_right(self, keyboard_interupt: str) -> None:
        """We turn the motor to the right"""
        if keyboard_interupt == "d":
            self.start()
            gpio.output(self.pins[1], gpio.HIGH)
            gpio.output(self.pins[2], gpio.LOW)
            gpio.output(self.pins[3], gpio.LOW)
            gpio.output(self.pins[4], gpio.LOW)
        return

    def turn_left(self, keyboard_interupt: str) -> None:
        """We turn the motor to the left"""
        if keyboard_interupt == "a":
            self.start()
            gpio.output(self.pins[1], gpio.LOW)
            gpio.output(self.pins[2], gpio.LOW)
            gpio.output(self.pins[3], gpio.HIGH)
            gpio.output(self.pins[4], gpio.HIGH)
        return

    def go_forward(self, keyboard_interupt: str) -> None:
        """We turn the motor forward"""
        if keyboard_interupt == "w":
            self.direction_forward = True
            self.start()
            gpio.output(self.pins[1], gpio.HIGH)
            gpio.output(self.pins[2], gpio.LOW)
            gpio.output(self.pins[3], gpio.HIGH)
            gpio.output(self.pins[4], gpio.LOW)
        return

    def go_back(self, keyboard_interupt: str) -> None:
        """We turn the motor backward"""
        if keyboard_interupt == "s":
            self.direction_forward = False
            self.start()
            gpio.output(self.pins[1], gpio.LOW)
            gpio.output(self.pins[2], gpio.HIGH)
            gpio.output(self.pins[3], gpio.LOW)
            gpio.output(self.pins[4], gpio.HIGH)

    def power_control(self, keyboard_interupt: str) -> None:
        """We control the power of the motor"""
        if keyboard_interupt == "u" and self.pwm_power < 90:
            self.pwm_power += 10
            self.pwm_controler.ChangeDutyCycle(self.pwm_power)
        elif keyboard_interupt == "i" and self.pwm_power > 90:
            self.pwm_power -= 10
            self.pwm_controler.ChangeDutyCycle(self.pwm_power)

    def stop(self) -> None:
        """We stop the motor"""
        self.pwm_controler1.ChangeDutyCycle(0)
        self.pwm_controler2.ChangeDutyCycle(0)

    def start(self) -> None:
        """We start the motor"""
        self.pwm_controler1.start(100)
        self.pwm_controler2.start(100)

    def getch(self) -> str:
        key = readchar.readkey()
        return str(key)

    def cleanup(self):
        if self.pwm_controler:
            self.pwm_controler1.stop()
            self.pwm_controler2.stop()
        for i in self.pins:
            gpio.output(i, gpio.LOW)
        gpio.cleanup()

    def working(self):
        button_delay = 0.1
        while True:
            char = self.getch()
            self.turn_right(char)
            self.turn_left(char)
            self.go_forward(char)
            self.go_back(char)
            self.power_control(char)
            if char == "e":
                break
            time.sleep(button_delay)
            self.stop()
        self.cleanup()


if __name__ == "__main__":
    machine = DevastatorMotorEngineManager()
    machine.working()
