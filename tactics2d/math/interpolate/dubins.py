import numpy as np

from tactics2d.math.geometry import Circle


class Dubins:
    """
    This class implements a Dubins curve interpolator.

    The curve comprises a sequence of three segments: RSR, RSL, LSL, LSR, RLR, and LRL. R stands for the right turn, L for the left turn, and S for the straight line. A Dubins path planner operates within the constraints of forward actions exclusively.

    Attributes:
        radius (float): The minimum turning radius of the vehicle.
    """

    def __init__(self, radius: float) -> None:
        self.radius = radius
        if self.radius <= 0:
            raise ValueError("The minimum turning radius must be positive.")

    def _RSR(self, alpha, beta, dist):
        discriminant = (
            2 + dist**2 - 2 * np.cos(alpha - beta) + 2 * dist * (-np.sin(alpha) + np.sin(beta))
        )

        if discriminant < 0:
            return None

        tmp = np.arctan2(np.cos(alpha) - np.cos(beta), dist - np.sin(alpha) + np.sin(beta))

        t = np.mod(alpha - tmp, 2 * np.pi)
        p = np.sqrt(discriminant)
        q = np.mod(-(beta - tmp), 2 * np.pi)

        return t, p, q

    def _RSL(self, alpha, beta, dist):
        discriminant = (
            -2 + dist**2 + 2 * np.cos(alpha - beta) - 2 * dist * (np.sin(alpha) + np.sin(beta))
        )

        if discriminant < 0:
            return None

        p = np.sqrt(discriminant)

        tmp = np.arctan2(
            np.cos(alpha) + np.cos(beta), dist - np.sin(alpha) - np.sin(beta)
        ) - np.arctan2(2, p)

        t = np.mod(alpha - tmp, 2 * np.pi)
        q = np.mod(beta - tmp, 2 * np.pi)

        return t, p, q

    def _LSL(self, alpha, beta, dist):
        discriminant = (
            2 + dist**2 - 2 * np.cos(alpha - beta) + 2 * dist * (np.sin(alpha) - np.sin(beta))
        )

        if discriminant < 0:
            return None

        tmp = np.arctan2(-np.cos(alpha) + np.cos(beta), dist + np.sin(alpha) - np.sin(beta))

        t = np.mod(-(alpha - tmp), 2 * np.pi)
        p = np.sqrt(discriminant)
        q = np.mod(beta - tmp, 2 * np.pi)

        return t, p, q

    def _LSR(self, alpha, beta, dist):
        discriminant = (
            -2 + dist**2 + 2 * np.cos(alpha - beta) + 2 * dist * (np.sin(alpha) + np.sin(beta))
        )

        if discriminant < 0:
            return None

        p = np.sqrt(discriminant)

        tmp = -np.arctan2(
            np.cos(alpha) + np.cos(beta), dist + np.sin(alpha) + np.sin(beta)
        ) + np.arctan2(2, p)

        t = np.mod(-alpha + tmp, 2 * np.pi)
        q = np.mod(-beta + tmp, 2 * np.pi)

        return t, p, q

    def _RLR(self, alpha, beta, dist):
        discriminant = (
            6 - dist**2 + 2 * np.cos(alpha - beta) + 2 * dist * (np.sin(alpha) - np.sin(beta))
        ) / 8

        if abs(discriminant) > 1:
            return None

        tmp = np.arctan2(np.cos(alpha) - np.cos(beta), dist - np.sin(alpha) + np.sin(beta))

        p = np.mod(2 * np.pi - np.arccos(discriminant), 2 * np.pi)
        t = np.mod(alpha - tmp + p / 2, 2 * np.pi)
        q = np.mod(alpha - beta - t + p, 2 * np.pi)

        return t, p, q

    def _LRL(self, alpha, beta, dist):
        discriminant = (
            6 - dist**2 + 2 * np.cos(alpha - beta) + 2 * dist * (-np.sin(alpha) + np.sin(beta))
        ) / 8

        if abs(discriminant) > 1:
            return None

        p = np.mod(2 * np.pi - np.arccos(discriminant), 2 * np.pi)

        tmp = np.arctan2(np.cos(alpha) - np.cos(beta), dist + np.sin(alpha) - np.sin(beta))

        t = np.mod(-alpha + tmp + p / 2, 2 * np.pi)
        q = np.mod(beta - alpha - t + p, 2 * np.pi)

        return t, p, q

    class Path:
        def __init__(self, segments, curve_type, radius):
            self.segments = segments
            self.curve_type = curve_type
            self.length = np.abs(segments).sum() * radius

    def _set_path(self, segments, curve_type):
        if segments is None:
            return None

        path = self.Path(segments, curve_type, self.radius)
        return path

    def get_all_path(
        self,
        start_point: np.ndarray,
        start_heading: float,
        end_point: np.ndarray,
        end_heading: float,
    ):
        """Get all the Dubins paths connecting two points.

        Args:
            start_point (np.ndarray): The start point of the curve. The shape is (2,).
            start_heading (float): The heading of the start point. The unit is radian.
            end_point (np.ndarray): The end point of the curve. The shape is (2,).
            end_heading (float): The heading of the end point. The unit is radian.
        """
        # create a new coordinate system with the start point as the origin
        theta = np.arctan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
        d = np.linalg.norm(end_point - start_point) / self.radius
        alpha = np.mod(start_heading - theta, 2 * np.pi)
        beta = np.mod(end_heading - theta, 2 * np.pi)

        paths = [
            self._set_path(self._LRL(alpha, beta, d), "LRL"),
            self._set_path(self._RLR(alpha, beta, d), "RLR"),
            self._set_path(self._LSL(alpha, beta, d), "LSL"),
            self._set_path(self._RSL(alpha, beta, d), "RSL"),
            self._set_path(self._RSR(alpha, beta, d), "RSR"),
            self._set_path(self._LSR(alpha, beta, d), "LSR"),
        ]

        return paths

    def get_path(
        self,
        start_point: np.ndarray,
        start_heading: float,
        end_point: np.ndarray,
        end_heading: float,
    ) -> Path:
        """
        Get the shortest Dubins path connecting two points.

        Args:
            start_point (np.ndarray): The start point of the curve. The shape is (2,).
            start_heading (float): The heading of the start point. The unit is radian.
            end_point (np.ndarray): The end point of the curve. The shape is (2,).
            end_heading (float): The heading of the end point. The unit is radian.
        """
        candidate_paths = self.get_all_path(start_point, start_heading, end_point, end_heading)

        shortest_path = None
        shortest_length = np.inf
        for path in candidate_paths:
            if path is None or path.length > shortest_length:
                continue
            else:
                shortest_length = path.length
                shortest_path = path

        return shortest_path

    def get_curve_line(
        self,
        path: Path,
        start_point: np.ndarray,
        start_heading: float,
        step_size: float = 0.1,
    ):
        def get_arc(point, heading, radius, radian, action):
            circle_center, _ = Circle.get_circle(
                Circle.ConstructBy.TangentVector, point, heading, radius, action
            )
            clockwise = action == "R"
            start_angle = (heading + np.pi / 2) if action == "R" else (heading - np.pi / 2)
            arc_curve = Circle.get_arc(
                circle_center,
                radius,
                radian,
                start_angle,
                clockwise,
                step_size,
            )

            end_angle = (start_angle - radian) if clockwise else (start_angle + radian)
            end_point = circle_center + np.array([np.cos(end_angle), np.sin(end_angle)]) * radius
            end_heading = (start_heading - radian) if clockwise else (start_heading + radian)

            return arc_curve, end_point, end_heading

        def get_straight_line(point, heading, radius, length):
            end_point = point + np.array([np.cos(heading), np.sin(heading)]) * radius * length
            x_step = step_size * np.cos(heading)
            y_step = step_size * np.sin(heading)
            x = np.arange(point[0], end_point[0], x_step)
            y = np.arange(point[1], end_point[1], y_step)
            straight_line = np.vstack((x, y)).T

            return straight_line, end_point, heading

        next_point = start_point
        next_heading = start_heading
        curves = []
        for i, action in enumerate(path.curve_type):
            if action == "S":
                curve, next_point, next_heading = get_straight_line(
                    next_point, next_heading, self.radius, abs(path.segments[i])
                )
            else:
                curve, next_point, next_heading = get_arc(
                    next_point, next_heading, self.radius, abs(path.segments[i]), action
                )
            curves.append(curve)

        return np.concatenate(curves)

    def get_curve(
        self,
        start_point: np.ndarray,
        start_heading: float,
        end_point: np.ndarray,
        end_heading: float,
        step_size: float = 0.1,
    ):
        """Get the shortest Dubins curve connecting two points.

        Args:
            start_point (np.ndarray): The start point of the curve. The shape is (2,).
            start_heading (float): The heading of the start point. The unit is radian.
            end_point (np.ndarray): The end point of the curve. The shape is (2,).
            end_heading (float): The heading of the end point. The unit is radian.
            step_size (float, optional): The step size of the curve. Defaults to 0.1.

        Returns:
            shortest_path (Path): The shortest Dubins path connecting two points.
            curve (np.ndarray): The shortest Dubins curve connecting two points.
        """

        shortest_path = self.get_path(start_point, start_heading, end_point, end_heading)
        curve = self.get_curve_line(shortest_path, start_point, start_heading, step_size)

        return shortest_path, curve
