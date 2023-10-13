import numpy as np

from tactics2d.math.geometry import Circle


class ReedsShepp:
    """
    This class implements a Reeds Shepp curve interpolator. The implementation follows the paper "Optimal paths for a car that goes both forwards and backwards" by Reeds and Shepp

    Attributes:
        radius (float): The minimum turning radius of the vehicle.
    ."""

    def __init__(self, radius: float) -> None:
        self.radius = radius
        if self.radius <= 0:
            raise ValueError("The minimum turning radius must be positive.")

    @staticmethod
    def _R(x, y):
        """Convert cartesian coordinates to polar coordinates."""
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        return r, theta

    @staticmethod
    def _M(theta):
        """Regulate a given angle to the range of [-pi, pi]."""
        phi = np.mod(theta, 2 * np.pi)

        if phi > np.pi:
            phi -= 2 * np.pi
        if phi < -np.pi:
            phi += 2 * np.pi

        return phi

    def _tau_omega(self, u, v, xi, eta, phi):
        """This function follows Equation 8.5 and 8.6 in the paper."""
        delta = self._M(u - v)
        A = np.sin(u) - np.sin(delta)
        B = np.cos(u) - np.cos(delta) - 1

        _, t1 = self._R(xi * A + eta * B, eta * A - xi * B)
        t2 = 2 * (np.cos(delta) - np.cos(v) - np.cos(u)) + 3

        tau = self._M(t1 + np.pi) if t2 < 0 else self._M(t1)
        omega = self._M(tau - u + v - phi)

        return tau, omega

    def _time_flip(self, x, y, phi):
        return (-x, y, -phi)

    def _reflect(self, x, y, phi):
        return (x, -y, -phi)

    def _backward(self, x, y, phi):
        x_ = x * np.cos(phi) + y * np.sin(phi)
        y_ = x * np.sin(phi) - y * np.cos(phi)
        return (x_, y_, phi)

    class Path:
        def __init__(self, segments, matrix, actions, curve_type, radius):
            self.actions = actions
            self.curve_type = curve_type

            t, u, v = segments
            self.segments = np.abs(
                np.dot(
                    np.array([t, u, v, 1])
                    if curve_type in ["CCSC", "CCSCC"]
                    else np.array([t, u, v]),
                    matrix,
                )
            )

            self.signs = np.sign(np.sum(matrix, axis=0))

            self.length = np.abs(self.segments).sum() * radius

    def _set_path(self, segments, matrix, actions, curve_type) -> Path:
        if segments is None:
            return None

        path = self.Path(segments, matrix, actions, curve_type, self.radius)
        return path

    def _CSC(self, x, y, phi):
        def LpSpLp(x, y, phi):
            """This function follows Equation 8.1 in the paper. It implements the L+S+L+ path, which can be converted to L-S-L-, R+S+R+, and R-S-R- by proper transformation."""
            u, t = self._R(x - np.sin(phi), y - 1 + np.cos(phi))

            if t < 0:
                return None

            v = self._M(phi - t)
            if v < 0:
                return None

            return (t, u, v)

        def LpSpRp(x, y, phi):
            """This function follows Equation 8.2 in the paper. It implements the L+S+R+ path, which can be converted to L-S-R-, R+S+L+, and R-S-L+ by proper transformation."""
            u1, t1 = self._R(x + np.sin(phi), y - 1 - np.cos(phi))

            if u1**2 < 4:
                return None

            u = np.sqrt(u1**2 - 4)
            _, theta = self._R(u, 2)
            t = self._M(t1 + theta)
            v = self._M(t - phi)

            if t < 0 or v < 0:
                return None

            return (t, u, v)

        inputs = [
            (x, y, phi),
            self._time_flip(*(x, y, phi)),
            self._reflect(*(x, y, phi)),
            self._time_flip(*(self._reflect(*(x, y, phi)))),
        ]

        # L+S+L+, L-S-L-, R+S+R+, R-S-R-, L+S+R+, L-S-R-, R+S+L+, R-S-L-
        paths = [
            self._set_path(LpSpLp(*inputs[0]), np.diag([1, 1, 1]), "LSL", "CSC"),
            self._set_path(LpSpLp(*inputs[1]), np.diag([-1, -1, -1]), "LSL", "CSC"),
            self._set_path(LpSpLp(*inputs[2]), np.diag([1, 1, 1]), "RSR", "CSC"),
            self._set_path(LpSpLp(*inputs[3]), np.diag([-1, -1, -1]), "RSR", "CSC"),
            self._set_path(LpSpRp(*inputs[0]), np.diag([1, 1, 1]), "LSR", "CSC"),
            self._set_path(LpSpRp(*inputs[1]), np.diag([-1, -1, -1]), "LSR", "CSC"),
            self._set_path(LpSpRp(*inputs[2]), np.diag([1, 1, 1]), "RSL", "CSC"),
            self._set_path(LpSpRp(*inputs[3]), np.diag([-1, -1, -1]), "RSL", "CSC"),
        ]

        return paths

    def _CCC(self, x, y, phi):
        def LpRnLp(x, y, phi):
            """This function is related to Equation 8.3. It implements the L+R-L+ path, which can be converted to L-R+L-, R+L-R+, and R-L+R- by proper transformation."""
            xi = x - np.sin(phi)
            eta = y - 1 + np.cos(phi)
            u1, theta = self._R(xi, eta)

            if u1 > 4:
                return None

            A = np.pi - np.arcsin(u1 / 4)
            t = self._M(theta + A)
            u = self._M(2 * A)
            v = self._M(phi - t + u)

            if t < 0 or u > 0 or v < 0:
                return None

            return (t, u, v)

        def LpRnLn(x, y, phi):
            """This function is related to Equation 8.4. It implements the L+R-L- path, which can be converted to L-R+L+, R+L-R-, and R-L+R+ by proper transformation."""
            xi = x - np.sin(phi)
            eta = y - 1 + np.cos(phi)
            u1, theta = self._R(xi, eta)

            if u1 > 4:
                return None

            A = np.arccos(u1 / 4)
            t = self._M(theta + A + np.pi / 2)
            u = self._M(np.pi - 2 * A)
            v = self._M(t + u - phi)

            return (t, u, v)

        def LpRpLn(x, y, phi):
            """This function is related to Equation 8.4. It implements the L+R+L- path, which can be converted to L-R-L+, R+L+R-, and R-L-R+ by proper transformation.

            This is the corrected version of the original paper. The paths L-R-L+, R+L+R-, and R-L-R+ are equivalent to L+R+L-, L-R-L+, and R+L+R-L- with adjusted order of actions.
            """
            xi = x + np.sin(phi)
            eta = y - 1 - np.cos(phi)
            u1, theta = self._R(-eta, xi)

            if u1 > 4:
                return None

            u = np.arccos(1 - u1**2 / 8)
            A = np.arcsin(2 * np.sin(u) / u1)
            t = self._M(theta - A + np.pi / 2)
            v = self._M(t - u - phi)

            return (t, u, v)

        inputs = [
            (x, y, phi),
            self._time_flip(*(x, y, phi)),
            self._reflect(*(x, y, phi)),
            self._time_flip(*(self._reflect(*(x, y, phi)))),
        ]

        matrix1 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        matrix2 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
        matrix3 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])

        # L+R-L+, L-R+L-, R+L-R+, R-L+R-, L+R-L-, L-R+L+, R+L-R-, R-L+R+
        paths = [
            self._set_path(LpRnLp(*inputs[0]), matrix1, "LRL", "CCC"),
            self._set_path(LpRnLp(*inputs[1]), -matrix1, "LRL", "CCC"),
            self._set_path(LpRnLp(*inputs[2]), matrix1, "RLR", "CCC"),
            self._set_path(LpRnLp(*inputs[3]), -matrix1, "RLR", "CCC"),
            #     self._set_path(LpRnLn(*inputs[0]), matrix2, "LRL", "CCC"),
            #     self._set_path(LpRnLn(*inputs[1]), -matrix2, "LRL", "CCC"),
            #     self._set_path(LpRnLn(*inputs[2]), matrix2, "RLR", "CCC"),
            #     self._set_path(LpRnLn(*inputs[3]), -matrix2, "RLR", "CCC"),
            #     self._set_path(LpRpLn(*inputs[0]), matrix3, "LRL", "CCC"),
            #     self._set_path(LpRpLn(*inputs[1]), -matrix3, "LRL", "CCC"),
            #     self._set_path(LpRpLn(*inputs[2]), matrix3, "RLR", "CCC"),
            #     self._set_path(LpRpLn(*inputs[3]), -matrix3, "RLR", "CCC"),
        ]

        return paths

    def _CCCC(self, x, y, phi):
        def LpRpLnRn(x, y, phi):
            """This function follows Equation 8.7. It implements the L+R+L-R- path, which can be converted to L-R-L+R+, R+L+R-L-, and R-L-R+L+ by proper transformation."""
            xi = x + np.sin(phi)
            eta = y - 1 - np.cos(phi)
            rho = (2 + np.sqrt(xi**2 + eta**2)) / 4

            if rho > 1 or rho < 0:
                return None

            u = np.arccos(rho)
            t, v = self._tau_omega(u, -u, xi, eta, phi)

            if t < 0 or v > 0:
                return None

            return (t, u, v)

        def LpRnLnRp(x, y, phi):
            """This function follows Equation 8.8. It implements the L+R-L-R+ path, which can be converted to L-R+L+R-, R+L-R-L+, and R-L+R-L+ by proper transformation."""
            xi = x + np.sin(phi)
            eta = y - 1 - np.cos(phi)
            rho = (20 - xi**2 - eta**2) / 16

            if rho > 1 or rho < 0:
                return None

            u = -np.arccos(rho)
            if u < -np.pi / 2:
                return None

            t, v = self._tau_omega(u, u, xi, eta, phi)

            if t < 0 or v < 0:
                return None

            return (t, u, v)

        inputs = [
            (x, y, phi),
            self._time_flip(*(x, y, phi)),
            self._reflect(*(x, y, phi)),
            self._time_flip(*(self._reflect(*(x, y, phi)))),
        ]

        matrix1 = np.array([[1, 0, 0, 0], [0, 1, -1, 0], [0, 0, 0, -1]])
        matrix2 = np.array([[1, 0, 0, 0], [0, -1, -1, 0], [0, 0, 0, 1]])

        # L+R+L-R-, L-R-L+R+, R+L+R-L-, R-L-R+L+, L+R-L+R-, L-R+L-R+, R+L-R-L-, R-L+R-L+
        paths = [
            self._set_path(LpRpLnRn(*inputs[0]), matrix1, "LRLR", "CCCC"),
            self._set_path(LpRpLnRn(*inputs[1]), -matrix1, "LRLR", "CCCC"),
            self._set_path(LpRpLnRn(*inputs[2]), matrix1, "RLRL", "CCCC"),
            self._set_path(LpRpLnRn(*inputs[3]), -matrix1, "RLRL", "CCCC"),
            self._set_path(LpRnLnRp(*inputs[0]), matrix2, "LRLR", "CCCC"),
            self._set_path(LpRnLnRp(*inputs[1]), -matrix2, "LRLR", "CCCC"),
            self._set_path(LpRnLnRp(*inputs[2]), matrix2, "RLRL", "CCCC"),
            self._set_path(LpRnLnRp(*inputs[3]), -matrix2, "RLRL", "CCCC"),
        ]

        return paths

    def _CCSC(self, x, y, phi):
        def LpRnSnLn(x, y, phi):
            """This function follows Equation 8.9. It implements the L+R-S-L- path, which can be converted to L-R+S+L+, R+L-S-R-, R-L+S+R+, L-S-R-L+, L+S+R+L-, R-S-L-R+, and R+S+L+R- by proper transformation."""
            xi = x - np.sin(phi)
            eta = y - 1 + np.cos(phi)
            rho, theta = self._R(xi, eta)

            if rho < 2:
                return None

            r = np.sqrt(rho**2 - 4)
            u = 2 - r
            t = self._M(theta + np.arctan2(r, -2))
            v = self._M(phi - np.pi / 2 - t)

            if t < 0 or u > 0 or v > 0:
                return None

            return (t, u, v)

        def LpRnSnRn(x, y, phi):
            """This function follows Equation 8.10. It implements the L+R-S-R- path, which can be converted to L-R+S+R+, R+L-S-L-, R-L+S+L+, R-S-R-L+, R+S+R+L-, L-S-L-R+, and L+S+L+R- by proper transformation."""
            xi = x + np.sin(phi)
            eta = y - 1 - np.cos(phi)
            rho, theta = self._R(-eta, xi)

            if rho < 2:
                return None

            t = theta
            u = 2 - rho
            v = self._M(t + np.pi / 2 - phi)

            if t < 0 or u > 0 or v > 0:
                return None

            return (t, u, v)

        inputs = [
            (x, y, phi),
            self._time_flip(*(x, y, phi)),
            self._reflect(*(x, y, phi)),
            self._time_flip(*(self._reflect(*(x, y, phi)))),
            self._backward(*(x, y, phi)),
            self._time_flip(*(self._backward(*(x, y, phi)))),
            self._reflect(*(self._backward(*(x, y, phi)))),
            self._time_flip(*(self._reflect(*(self._backward(*(x, y, phi)))))),
        ]

        matrix1 = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1], [0, -np.pi / 2, 0, 0]])
        matrix2 = np.array([[0, 0, 0, 1], [0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, -np.pi / 2, 0]])

        # L+R-S-L-, L-R+S+L+, R+L-S-R-, R-L+S+R+, L-S-R-L+, L+S+R+L-, R-S-L-R+, R+S+L+R-
        # L+R-S-R-, L-R+S+R+, R+L-S-L-, R-L+S+L+, R-S-R-L+, R+S+R+L-, L-S-L-R-, L+S+L+R-,
        paths = [
            self._set_path(LpRnSnLn(*inputs[0]), matrix1, "LRSL", "CCSC"),
            self._set_path(LpRnSnLn(*inputs[1]), -matrix1, "LRSL", "CCSC"),
            self._set_path(LpRnSnLn(*inputs[2]), matrix1, "RLSR", "CCSC"),
            self._set_path(LpRnSnLn(*inputs[3]), -matrix1, "RLSR", "CCSC"),
            self._set_path(LpRnSnLn(*inputs[4]), matrix2, "LSRL", "CCSC"),
            self._set_path(LpRnSnLn(*inputs[5]), -matrix2, "LSRL", "CCSC"),
            self._set_path(LpRnSnLn(*inputs[6]), matrix2, "RSLR", "CCSC"),
            self._set_path(LpRnSnLn(*inputs[7]), -matrix2, "RSLR", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[0]), matrix1, "LRSR", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[1]), -matrix1, "LRSR", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[2]), matrix1, "RLSL", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[3]), -matrix1, "RLSL", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[4]), matrix2, "RSRL", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[5]), -matrix2, "RSRL", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[6]), matrix2, "LSLR", "CCSC"),
            self._set_path(LpRnSnRn(*inputs[7]), -matrix2, "LSLR", "CCSC"),
        ]

        return paths

    def _CCSCC(self, x, y, phi):
        def LpRnSnLnRp(x, y, phi):
            """This function follows Equation 8.11. It implements the L+R-S-L-R+ path, which can be converted to L-R+S+L+R-, R+L-S-R-L+, and R-L+S+R+L- by proper transformation."""
            xi = x + np.sin(phi)
            eta = y - 1 - np.cos(phi)
            rho, theta = self._R(xi, eta)

            if rho < 2:
                return None

            t = self._M(theta - np.arccos(-2 / rho))

            if t <= 0:
                return None

            u = 4 - (xi + 2 * np.cos(t)) / np.sin(t)
            v = self._M(t - phi)

            if u > 0 or v < 0:
                return None

            return (t, u, v)

        inputs = [
            (x, y, phi),
            self._time_flip(*(x, y, phi)),
            self._reflect(*(x, y, phi)),
            self._time_flip(*(self._reflect(*(x, y, phi)))),
        ]

        matrix = np.array(
            [[1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, -np.pi / 2, 0, -np.pi / 2, 0]]
        )

        # L+R-S-L-R+, L-R+S+L+R-, R+L-S-R-L+, R-L+S+R+L-
        paths = [
            self._set_path(LpRnSnLnRp(*inputs[0]), matrix, "LRSLR", "CCSCC"),
            self._set_path(LpRnSnLnRp(*inputs[1]), -matrix, "LRSLR", "CCSCC"),
            self._set_path(LpRnSnLnRp(*inputs[2]), matrix, "RLSRL", "CCSCC"),
            self._set_path(LpRnSnLnRp(*inputs[3]), -matrix, "RLSRL", "CCSCC"),
        ]

        return paths

    def get_all_path(
        self,
        start_point: np.ndarray,
        start_heading: float,
        end_point: np.ndarray,
        end_heading: float,
    ) -> list:
        """Get all the Reeds-Shepp paths connecting two points.

        Args:
            start_point (np.ndarray): The start point of the curve. The shape is (2,).
            start_heading (float): The start heading of the curve.
            end_point (np.ndarray): The end point of the curve. The shape is (2,).
            end_heading (float): The end heading of the curve.
        """
        dx = (end_point[0] - start_point[0]) / self.radius
        dy = (end_point[1] - start_point[1]) / self.radius
        x = dx * np.cos(start_heading) + dy * np.sin(start_heading)
        y = -dx * np.sin(start_heading) + dy * np.cos(start_heading)
        phi = end_heading - start_heading

        paths = (
            self._CCC(x, y, phi)
            + self._CSC(x, y, phi)
            + self._CCSC(x, y, phi)
            + self._CCCC(x, y, phi)
            + self._CCSCC(x, y, phi)
        )

        return paths

    def get_path(
        self,
        start_point: np.ndarray,
        start_heading: float,
        end_point: np.ndarray,
        end_heading: float,
    ):
        """Get the shortest Reeds-Shepp path connecting two points.

        Args:
            start_point (np.ndarray): The start point of the curve. The shape is (2,).
            start_heading (float): The start heading of the curve.
            end_point (np.ndarray): The end point of the curve. The shape is (2,).
            end_heading (float): The end heading of the curve.
        """
        candidate_paths = self.get_all_path(start_point, start_heading, end_point, end_heading)

        shortest_path = None
        shortest_length = np.inf
        for path in candidate_paths:
            if path is None or path.length > shortest_length:
                continue
            else:
                shortest_path = path
                shortest_length = path.length

        return shortest_path

    def get_curve_line(
        self, path: Path, start_point: np.ndarray, start_heading: float, step_size: float = 0.01
    ):
        def get_arc(point, heading, radius, radian, forward, action):
            circle_center, _ = Circle.get_circle(
                Circle.ConstructBy.TangentVector, point, heading, radius, action
            )
            start_angle = (heading + np.pi / 2) if action == "R" else (heading - np.pi / 2)
            clockwise = (action == "R" and forward > 0) or (action == "L" and forward < 0)
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
            end_heading = (heading - radian) if clockwise else (heading + radian)

            return arc_curve, end_point, end_heading

        def get_straight_line(point, heading, radius, length, forward):
            end_point = (
                point + np.array([np.cos(heading), np.sin(heading)]) * radius * length * forward
            )
            x_step = step_size * np.cos(heading) * forward
            y_step = step_size * np.sin(heading) * forward
            x = np.arange(point[0], end_point[0], x_step)
            y = np.arange(point[1], end_point[1], y_step)
            straight_line = np.array([x, y]).T

            return straight_line, end_point, heading

        next_point = start_point
        next_heading = start_heading
        curves = []
        for i, action in enumerate(path.actions):
            if action == "S":
                curve, next_point, next_heading = get_straight_line(
                    next_point, next_heading, self.radius, path.segments[i], path.signs[i]
                )
            else:
                curve, next_point, next_heading = get_arc(
                    next_point,
                    next_heading,
                    self.radius,
                    abs(path.segments[i]),
                    path.signs[i],
                    action,
                )
            curves.append(curve)

        return np.concatenate(curves)

    def get_curve(
        self,
        start_point: np.ndarray,
        start_heading: float,
        end_point: np.ndarray,
        end_heading: float,
        step_size: float = 0.01,
    ):
        """Get the shortest Reeds-Shepp curve connecting two points.

        Args:
            start_point (np.ndarray): The start point of the curve. The shape is (2,).
            start_heading (float): The start heading of the curve.
            end_point (np.ndarray): The end point of the curve. The shape is (2,).
            end_heading (float): The end heading of the curve.
        """
        shortest_path = self.get_path(start_point, start_heading, end_point, end_heading)
        curve = self.get_curve_line(shortest_path, start_point, start_heading, step_size)

        return shortest_path, curve
