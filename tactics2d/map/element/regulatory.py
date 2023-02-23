from typing import List, Tuple


class RegulatoryElement(object):
    """tactics2d.map.element.RegulatoryElement

    The attributes of Regulatory refers to
    https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/RegulatoryElementTagging.md
    
    Attrs:
        subtype (str): By default it is one of [traffic_sign, traffic_light, speed_limit,
            right_of_way, all_way_stop]
        member_list
        dynamic (bool): Indicates that this Regulatory Element might change its meaning based
            on a condition.
        fallback (bool): Indicates that this Regulatory Element has a lower priority than another
            Regulatory Element.
    """
    # TODO: Process Regulatory Information
    def __init__(
        self, id_: str, 
        relation_list: List[Tuple[str, str]] = None, way_list: List[Tuple[str, str]] = None,
        type_: str = "regulatory_element", subtype: str = None, location: str = None,
        dynamic: bool = False, fallback: bool = False,
        custom_tags: dict = None
    ):
        
        if subtype is None:
            raise ValueError("The subtype of RegulatoryElement %s is not defined!" % id_)

        self.id_ = id_
        self.type_ = type_
        self.subtype = subtype
        self.location = location
        self.relation_list = relation_list
        self.way_list = way_list
        self.dynamic = dynamic
        self.fallback = fallback
        self.custom_tags = custom_tags