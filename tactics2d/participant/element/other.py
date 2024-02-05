##! python3
# -*- coding: utf-8 -*-
# Copyright (C) 2024, Tactics2D Authors. Released under the GNU GPLv3.
# @File: other.py
# @Description: This file defines a class for a traffic participant of an unknown type.
# @Author: Yueyuan Li
# @Version: 1.0.0

import numpy as np
from shapely.geometry import LinearRing
from shapely.affinity import affine_transform

from .participant_base import ParticipantBase
from tactics2d.participant.trajectory.trajectory import Trajectory


class Other(ParticipantBase):
    """This class defines a dynamic traffic participant of an unknown type.

    Attributes:

    """

    def __init__(self, id_: int, type_: str = None, **kwargs):
        super().__init__(id_, type_, **kwargs)

        if not hasattr(self, "shape"):
            if not self.length is None and not self.width is None:
                self.shape = LinearRing(
                    [
                        [0.5 * self.length, -0.5 * self.width],
                        [0.5 * self.length, 0.5 * self.width],
                        [-0.5 * self.length, 0.5 * self.width],
                        [-0.5 * self.length, -0.5 * self.width],
                    ]
                )

    def _verify_trajectory(self, trajectory: Trajectory) -> bool:
        return True

    def bind_trajectory(self, trajectory: Trajectory):
        if self._verify_trajectory(trajectory):
            self.trajectory = trajectory
        else:
            raise RuntimeError()

    def get_pose(self, frame: int = None) -> LinearRing:
        state = self.trajectory.get_state(frame)
        transform_matrix = [
            np.cos(state.heading),
            -np.sin(state.heading),
            np.sin(state.heading),
            np.cos(state.heading),
            state.location[0],
            state.location[1],
        ]
        return affine_transform(self.shape, transform_matrix)

    def get_trace(self, frame_range=None):
        return None
