#!/usr/bin/python3
import DevastatorMotorEngineManager
import CameraManager1
import multiprocessing
import threading


def motor_process():
    motor = DevastatorMotorEngineManager.DevastatorMotorEngineManager()
    motor.working()


def camera_thread():
    camera = camera_manager1.CameraManager()
    camera.working()


if __name__ == "__main__":
    motor_process = multiprocessing.Process(target=motor_process, deamon=True)
    camera_thread = threading.Thread(target=camera_thread, daemon=True)
    motor_process.start()
    camera_thread.start()
