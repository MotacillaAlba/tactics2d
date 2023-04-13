from typing import Tuple

import numpy as np


class Circle:
    """_summary_"""

    @staticmethod
    def get_circle(pt1, pt2, pt3) -> Tuple[list, float]:
        """Derive a circle by three points.

        Returns:
            center (list): The center of the circle
            radius (float): The radius of the circle
        """
        d = -np.linalg.det(
            [
                [pt1[0] ** 2 + pt1[1] ** 2, pt1[1], 1],
                [pt2[0] ** 2 + pt2[1] ** 2, pt2[1], 1],
                [pt3[0] ** 2 + pt3[1] ** 2, pt3[1], 1],
            ]
        )
        e = np.linalg.det(
            [
                [pt1[0] ** 2 + pt1[1] ** 2, pt1[0], 1],
                [pt2[0] ** 2 + pt2[1] ** 2, pt2[0], 1],
                [pt3[0] ** 2 + pt3[1] ** 2, pt3[0], 1],
            ]
        )
        det = np.linalg.det(
            [[pt1[0], pt1[1], 1], [pt2[0], pt2[1], 1], [pt3[0], pt3[1], 1]]
        )

        D = d / det
        E = e / det

        center = [-D / 2, -E / 2]
        radius = np.linalg.norm(pt1 - center)

        return center, radius
