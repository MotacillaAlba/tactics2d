from abc import ABC, abstractmethod

from shapely.geometry import LineString

from .traffic_event import TrafficEvent


class ScenarioManager(ABC):
    """The base class for scenario managers.

    The scenario manager is used to reset a scenario (including the map, agent, and 
        participants), update the state of the traffic participants, and check the traffic events.

    Attributes:
        n_step (int): The current time step.
        max_step (int): The maximum time step.
        status (TrafficEvent): The status of the agent.
        map_ (Map): The map of the scenario.
        participants (list): The list of traffic participants.
        agent (Vehicle): The controllable vehicle in the scenario.
    """
    def __init__(self, max_step: int):
        self.n_step = 0
        self.max_step = max_step
        self.status = TrafficEvent.NORMAL

        self.map_ = None
        self.participants = None
        self.agent = None

    @abstractmethod
    def update(self):
        """Update the state of the traffic participants.
        """

    @abstractmethod
    def reset(self):
        """Reset the scenario."""
        
    def _check_time_exceeded(self):
        """Check if the simulation has reached the maximum time step.
        """
        if self.n_step > self.max_step:
            self.status = TrafficEvent.TIME_EXCEED

    def _check_retrograde(self):
        """Check if the agent is driving in the opposite direction of the lane.
        """
        return TrafficEvent.VIOLATION_RETROGRADE
    
    def _check_non_drivable(self):
        """Check if the agent is driving on the non-drivable area.
        """
        return TrafficEvent.VIOLATION_NON_DRIVABLE
    
    def _check_outbound(self):
        """Check if the agent is outside the map boundary.
        """
        map_boundary = LineString([
            (self.map_.boundary[0], self.map_.boundary[2]),
            (self.map_.boundary[0], self.map_.boundary[3]),
            (self.map_.boundary[1], self.map_.boundary[3]),
            (self.map_.boundary[1], self.map_.boundary[2])
        ])

        if not map_boundary.contains(self.agent.get_pose(self.n_step)):
            self.status = TrafficEvent.OUTSIDE_MAP

    def _check_collision(self):
        """Check if the agent collides with other participants or the static obstacles."""
        agent_pose = self.agent.get_pose(self.n_step)

        for participant in self.participants:
            participant_pose = participant.get_pose()
            if agent_pose.intersection(participant_pose).area > 0:
                if participant.type_ == "pedestrian":
                    self.status = TrafficEvent.COLLISION_PEDESTRIAN
                    return
                elif participant.type_ == "vehicle":
                    self.status = TrafficEvent.COLLISION_VEHICLE
                    return

        return TrafficEvent.NORMAL

    @abstractmethod
    def _check_complete(self):
        """Check if the goal of this scenario is reached.
        """

    @abstractmethod
    def check_status(self) -> TrafficEvent:
        """Detect different traffic events and return the status.

        If the status is normal, the simulation will continue. Otherwise, the simulation 
            will be terminated and the status will be returned. If multiple traffic events
            happen at the same step, only the event with the highest priority will be returned.
        """