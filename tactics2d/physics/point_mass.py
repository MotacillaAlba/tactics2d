from typing import Tuple

import numpy as np

from .base import VehiclePhysicsBase
from tactics2d.trajectory.element import State


class PointMass(VehiclePhysicsBase):
    """An implementation of the point-mass model.

    The implementation is specified for the purpose of updating and verifying the vehicle's state.

    TODO:
    - implement speed limit
    - implement state validation

    Attributes:
        time_step (float): _description_
        steering_angle_range (Tuple[float, float], optional): _description_. Defaults to None.
        speed_range (Tuple[float, float], optional): _description_. Defaults to None.
        accel_range (Tuple[float, float], optional): _description_. Defaults to None.
    """

    def __init__(
        self,
        time_step: float,
        steering_angle_range: Tuple[float, float] = None,
        speed_range: Tuple[float, float] = None,
        accel_range: Tuple[float, float] = None,
    ):
        super().__init__(time_step, steering_angle_range, speed_range, accel_range)

    def update(self, state: State, action) -> State:
        if self.accel_range is not None:
            accel = np.clip(action.accel, self.accel_range[0], self.accel_range[1])
        else:
            accel = action.accel
        if self.steering_angle_range is not None:
            steering = np.clip(action.steering, self.steering_angle_range)
        else:
            steering = action.steering

        new_ax = accel * np.sin(steering)
        new_ay = accel * np.cos(steering)
        new_vx = state.vx + new_ax * self.time_step
        new_vy = state.vy + new_ay * self.time_step
        new_x = state.x + self.vx * self.time_step + 0.5 * self.ax * self.time_step**2
        new_y = state.y + self.vy * self.time_step + 0.5 * self.ay * self.time_step**2
        new_heading = np.arctan2(new_vy, new_vx)

        new_state = State(
            state.timestamp + self.time_step,
            new_heading,
            new_x,
            new_y,
            new_vx,
            new_vy,
            new_ax,
            new_ay,
        )

        return new_state

    def verify(self, state: State, action) -> bool:
        return True
