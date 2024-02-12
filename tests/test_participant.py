##! python3
# -*- coding: utf-8 -*-
# Copyright (C) 2024, Tactics2D Authors. Released under the GNU GPLv3.
# @File: test_participant.py
# @Description:
# @Author: Yueyuan Li
# @Version: 1.0.0

import sys

from build.lib import trajectory

sys.path.append(".")
sys.path.append("..")

import os
from io import StringIO
import time
import logging

import pytest

from tactics2d.participant.element import (
    ParticipantBase,
    Vehicle,
    Cyclist,
    Pedestrian,
    Other,
    list_vehicle_templates,
    list_cyclist_templates,
    list_pedestrian_templates,
)
from tactics2d.participant.trajectory import Trajectory, State


@pytest.mark.participant
def test_printers():
    print_output = StringIO()
    sys.stdout = print_output
    print()
    for func in [list_vehicle_templates, list_cyclist_templates, list_pedestrian_templates]:
        func()

    logging.info(print_output.getvalue())
    sys.stdout = sys.__stdout__


@pytest.mark.participant
def test_participant_base():
    class TestParticipant(ParticipantBase):
        def __init__(self, id_, type_="test", **kwargs):
            super().__init__(id_, type_, **kwargs)

        @property
        def geometry(self):
            return None

        def bind_trajectory(self):
            return

        def get_pose(self):
            return

        def get_trace(self):
            return

    class_instance = TestParticipant(0)
    class_instance.add_state(State(0, 5, 6, 0.5))
    class_instance.add_state(State(100, 6, 8, 0.8))
    class_instance.get_pose()
    logging.info(class_instance.geometry)
    logging.info(class_instance.get_trace())
    assert class_instance.id_ == 0


@pytest.mark.participant
@pytest.mark.parametrize(
    "class_, type_name, overwrite, attributes",
    [
        (Vehicle, "small_car", True, {"max_speed": 52.78}),
        (Vehicle, "small_car", False, {"max_speed": 55.56}),
        (Vehicle, "S", True, {"max_speed": 63.89}),
        (Vehicle, "no_exist", True, {"max_speed": 55.56}),
        (Cyclist, "motorcycle", True, {"max_accel": 5.0}),
        (Cyclist, "motorcycle", False, {"max_accel": 5.8}),
        (Pedestrian, "adult_female", True, {"height": 1.65}),
        (Pedestrian, "adult_female", False, {"height": 1.75}),
    ],
)
def test_load_template(class_, type_name: str, overwrite: bool, attributes: dict):
    class_instance = class_(0)
    class_instance.load_from_template(type_name, overwrite)
    for key, value in attributes.items():
        assert getattr(class_instance, key) == value


@pytest.mark.participant
@pytest.mark.parametrize("class_", [Vehicle, Cyclist, Pedestrian, Other])
def test_functions(class_):
    # TODO: This test currently serves to increase the test coverage percentage. There is space for future improvements.
    class_instance = class_(0, length=4, width=3, height=5)
    class_instance.add_state(State(0, 5, 6, 0.5))
    class_instance.add_state(State(100, 6, 8, 0.8))
    class_instance.get_pose()
    logging.info(class_instance.geometry)
    logging.info(class_instance.get_trace())
