#!/usr/bin/python3
import DevastatorMotorEngineManager
import CameraManager1
import multiprocessing
import threading


def motor_task():
    motor = DevastatorMotorEngineManager.DevastatorMotorEngineManager()
    motor.working()


def camera_task():
    camera = CameraManager1.CameraManager()
    camera.working()


if __name__ == "__main__":
    motor_thread = threading.Thread(target=motor_task, daemon=True)
    camera_thread = threading.Thread(target=camera_task, daemon=True)
    motor_thread.start()
    camera_thread.start()
    motor_thread.join()
    camera_thread.join()
