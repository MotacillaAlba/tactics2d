import warnings
from enum import Enum

from shapely.geometry import LineString, LinearRing

from .defaults import LEGAL_SPEED_UNIT


class Relationship(Enum):
    PREDECESSOR = 1
    SUCCESSOR = 2
    LEFT_NEIGHBOR = 3
    RIGHT_NEIGHBOR = 4


class Lane(object):
    """## tactics2d.map.element.Lane

    An implementation of the lanelet2-style lanelet with neighbors detected.

    The detailed definition of the lanelet2-style lanelet can be found here:
    https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletPrimitives.md

    Attributes:
        id_ (str): _description_
        left_side (LineString): _description_
        right_side (LineString): _description_
        line_ids (set, optional): the ids of the roadline components. Defaults to None.
        subtype (str, optional): _description_. Defaults to None.
        location (str, optional): _description_. Defaults to None.
        inferred_participants (list, optional): _description_. Defaults to None.
        speed_limit (float, optional): _description_. Defaults to None.
        speed_limit_unit (str, optional): _description_. Defaults to "km/h".
        speed_limit_mandatory (bool, optional): _description_. Defaults to True.
        predecessors (set):
        successors (set):
        left_neighbors (set):
        right_neighbors (set):
    """
    def __init__(
        self, id_: str, left_side: LineString, right_side: LineString, line_ids: set = None,
        type_: str = "lanelet", subtype: str = None, color: tuple = None, location: str = None,
        inferred_participants: list = None,
        speed_limit: float = None, speed_limit_unit: str = "km/h",
        speed_limit_mandatory: bool = True,
        custom_tags: dict = None
    ):

        self.id_ = id_
        self.left_side = left_side
        self.right_side = right_side
        self.line_ids = line_ids
        self.type_ = type_
        self.subtype = subtype
        self.color = color
        self.location = location
        self.inferred_participants = inferred_participants
        self.speed_limit = speed_limit
        self.speed_limit_unit = speed_limit_unit
        self.speed_limit_mandatory = speed_limit_mandatory
        self.custom_tags = custom_tags

        self.polygon = LinearRing(list(self.left_side.coords) + list(reversed(list(self.right_side.coords))))

        self.predecessors = set()
        self.successors = set()
        self.left_neighbors = set()
        self.right_neighbors = set()

    @property
    def starts(self) -> list:
        """Return start points of the lane
        """
        return [self.left_side.coords[0], self.right_side.coords[0]]

    @property
    def ends(self) -> list:
        """Return the end points of the lane
        """
        return [self.left_side.coords[-1], self.right_side.coords[-1]]

    @property
    def shape(self) -> list:
        """Return the shape of the lane
        """
        return list(self.polygon.coords)

    def is_valid(self) -> bool:
        """
        """
        if self.speed_limit_unit not in LEGAL_SPEED_UNIT:
            warnings.warn(
                "Invalid speed limit unit %s. The legal units types are %s" % \
                (self.speed_limit_unit, ", ".join(LEGAL_SPEED_UNIT))
            )

    def is_related(self, id_: str) -> Relationship:
        """Check if a given lane is related to the lane

        Args:
            id_ (str): The given lane's id.
        """
        if id_ in self.predecessors:
            return Relationship.PREDECESSOR
        elif id_ in self.successors:
            return Relationship.SUCCESSOR
        elif id_ in self.left_neighbors:
            return Relationship.LEFT_NEIGHBOR
        elif id_ in self.right_neighbors:
            return Relationship.RIGHT_NEIGHBOR

    def add_related_lane(self, id_: str, relationship: Relationship):
        """Add a related lane's id to the corresponding list

        Args:
            id_ (str): the related lane's id
            relationship (Relationship): the relationship of the lanes
        """
        if id_ == self.id_:
            warnings.warn(f"Lane {self.id_} cannot be a related lane to itself.")
            return
        if relationship == Relationship.PREDECESSOR:
            self.predecessors.add(id_)
        elif relationship == Relationship.SUCCESSOR:
            self.successors.add(id_)
        elif relationship == Relationship.LEFT_NEIGHBOR:
            self.left_neighbors.add(id_)
        elif relationship == Relationship.RIGHT_NEIGHBOR:
            self.right_neighbors.add(id_)