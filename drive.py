import math
import time

# pylint: disable=import-error
import cv2
import numpy as np
import matplotlib.pyplot as plt
from machathon_judge import Simulator, Judge
import keyboard
from perception import perception
from control import control


class FPSCounter:


    def __init__(self):
        self.frames = []

    def step(self):
        self.frames.append(time.monotonic())

    def get_fps(self):
        n_seconds = 5

        count = 0
        cur_time = time.monotonic()
        for f in self.frames:
            if cur_time - f < n_seconds:  # Count frames in the past n_seconds
                count += 1

        return count / n_seconds
def run_car(simulator: Simulator) -> None:
    """
        simulator : Simulator
        The simulator object to control the car
        The only functions that should be used are:
        - get_image()
        - set_car_steering()
        - set_car_velocity()
        - get_state()
    """
    fps_counter.step()

    # Get the image and show it
    img = simulator.get_image()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    fps = fps_counter.get_fps()
    # draw fps on image
    cv2.putText( 
        img,
        f"FPS: {fps:.2f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("Live", perception(img)[0])
    steeringRatio , throttleRatio =control(img,perception(img)[1])
    cv2.waitKey(1)
    # steeringRatio = 0
    # if keyboard.is_pressed("a"):
    #     steeringRatio = 0.2
    # elif keyboard.is_pressed("d"):
    #     steeringRatio = -0.2

    # throttleRatio = 1
    # if keyboard.is_pressed("w"):
    #     throttleRatio = 1
    # elif keyboard.is_pressed("s"):
    #     throttleRatio = -1
       

    simulator.set_car_steering(steeringRatio * simulator.max_steer_angle / 1.7)
    simulator.set_car_velocity(throttleRatio * 25)


if __name__ == "__main__":
    # Initialize any variables needed
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    fps_counter = FPSCounter()

    # You should modify the value of the parameters to the judge constructor
    # according to your team's info
    judge = Judge(team_code="your_new_team_code", zip_file_path="your_solution.zip")

    # Pass the function that contains your main solution to the judge
    judge.set_run_hook(run_car)

    # Start the judge and simulation
    judge.run(send_score=False, verbose=True)