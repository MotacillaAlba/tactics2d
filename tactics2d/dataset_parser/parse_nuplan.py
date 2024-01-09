import os
from typing import Tuple

import sqlite3

from tactics2d.participant.element import Vehicle, Pedestrian, Cyclist, Other
from tactics2d.trajectory.element import State, Trajectory
from tactics2d.map.element import Map


class NuPlanParser:
    """This class implements a parser for NuPlan dataset.

    Caesar, Holger, et al. "nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles." arXiv preprint arXiv:2106.11810 (2021).
    """

    CLASS_MAPPING = {
        "vehicle": Vehicle,
        "bicycle": Cyclist,
        "pedestrian": Pedestrian,
        "traffic_cone": Other,
        "barrier": Other,
        "czone_sign": Other,
        "generic_object": Other,
    }

    def parse_trajectory(
        self, file_name: str, folder_path: str, stamp_range: Tuple[float, float] = None
    ):
        """This function parses trajectories from a single NuPlan database file.

        Args:
            file_name (str): _description_
            folder_path (str): _description_
            stamp_range (Tuple[float, float], optional): The time range of the trajectory data to parse. If the stamp range is not given, the parser will parse the whole trajectory data. Defaults to None.

        Returns:
            dict: A dictionary of participants. The keys are the ids of the participants. The values are the participants.
        """
        file_path = os.path.join(folder_path, file_name)

        if stamp_range is None:
            stamp_range = (-float("inf"), float("inf"))

        participants = dict()

        with sqlite3.connect(file_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM track;")
            rows = cursor.fetchall()

            for row in rows:
                category_token = row[1]
                cursor.execute("SELECT * FROM category WHERE token=?;", (category_token,))
                category_name = cursor.fetchone()[1]
                participants[row[0]] = self.CLASS_MAPPING[category_name](
                    id_=row[0],
                    type_=category_name,
                    length=row[3],
                    width=row[2],
                    height=row[4],
                    trajectory=Trajectory(id_=row[0], fps=20, stable_freq=False),
                )

            cursor.execute("SELECT * FROM lidar_box;")
            rows = cursor.fetchall()

            for row in rows:
                cursor.execute("SELECT * FROM lidar_pc WHERE token=?;", (row[1],))
                timestamp = cursor.fetchone()[7]
                if timestamp < stamp_range[0] or timestamp > stamp_range[1]:
                    continue
                state = State(
                    frame=timestamp, x=row[5], y=row[6], heading=row[14], vx=row[11], vy=row[12]
                )
                participants[row[2]].trajectory.append_state(state)

        cursor.close()
        connection.close()
        return participants

    def parse_map(self):
        return
