from dataclasses import dataclass

@dataclass
class Place:
    """
    Class that stores basic information about the place
    Parent class to PointPOfInterest and Lodging

    :name: name of place
    :place_id: Google's unique id for a place
    :lat: latitude of coordinates
    :lng: longitude of coordinates
    :address: address or vicinity of place
    """
    name: str
    place_id: str
    lat: float
    lng: float
    address: str

@dataclass
class PointOfInterest(Place):
    """
    Class that stores information about the point of interest
    Child class to Place

    :used_in_search: see if the point of interest should be used when finding lodgings
    """
    used_in_search: bool = True

    def switch_used_in_search(self):
        """
        Changes used_in_search to opposite value
        True -> False
        False -> True
        """
        self.used_in_search = not self.used_in_search

@dataclass
class Lodging(Place):
    """
    Class that stores information about the lodging
    Child class to Place

    :rating: average rating given by Google's reviews
    :number_of_ratings: total number of revies of the place
    """
    rating: float
    number_of_ratings: int