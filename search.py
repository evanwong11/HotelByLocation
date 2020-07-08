import google_api

# move below functions for better readability???
def truncate_coords(coordinates):
    """
    Truncates coordinates to maximum 8 decimal places.
    Removes extra trailing 0's and decimal point

    :coordinates: Either one lat or long coordinate
        :ex: "12.", "12.000000", "12.3456789123"
        :type: float

    :return: Truncated lat or long coordinate
        :ex: "12", "12", "12.34567891"
        :type: str
    """
    return f'{coordinates:.8f}'.rstrip('0').rstrip('.')

def miles_to_meters(miles):
    """
    Converts miles to meters

    :miles: distance
        :type: float

    :return: distance in meteres
        :type: float
    """
    return miles * 1609.344

def meters_to_miles(meters):
    """
    Converts meters to miles

    :meters: distance
        :type: float

    :return: distance in miles
        :type: float
    """
    return meters / 1609.344

class Search:
    """
    Class that contains the users search parameters
    """

    def __init__(self, lodging_type, location, radius):
        """
        :lodging_type: 'hotel' or 'hostel'
            :type: str

        :location: name of the location; ex: "Paris, France"
            :type: str

        :radius: range of search in meters
            :Note: max allowed by Google Maps is 50,000 meters
            :type: int

        :point_of_interests: places that the user wants to see
            :type: dict

        :lodgings: lodges found based on search
            :type: dict

        :central_point: average coordinates based on chosen point of interests
            :type: str

        :page_token: token for looking up additional lodging results
            :Note: only given if there are more than 20 results
                   max search results is 60
            :type: str
        """
        self.lodging_type = lodging_type
        self.location = location
        self.radius = radius if radius <= 50000 else 50000
        self.point_of_interests = dict()
        self.lodgings = dict()
        self.central_point = ''
        self.page_token = ''

    def add_point_of_interests(self, poi):
        """
        Add a point of interest

        :poi: name or address of the point of interest
            :type: str
        """
        self.point_of_interests[poi] = google_api.point_of_interest_search(poi)

    def delete_point_of_interest(self, poi):
        """
        Deletes a point of interest

        :poi: name or address of the point of interest
            :type: str
        """
        self.point_of_interests.pop(poi)

    def change_point_of_interest_in_search(self, poi):
        """
        Changes point of interest to be used in the search

        :poi: name or address of the point of interest
        """
        self.point_of_interests[poi].switch_used_in_search()

    def add_lodging(self):
        """
        Add the found lodgings from the search
        """
        results, self.page_token = google_api.lodging_search()
        for i in results:
            self.lodgings[i.place_id] = i

    def clear_lodgings(self):
        """
        Clears all hotels from the search
        """
        self.lodgings.clear()

    def find_central_point(self):
        """
        Finds the central point between the point of interests
        """
        lat_total = 0
        lon_total = 0
        number_of_locations = len(self.point_of_interests)
        for poi in self.point_of_interests:
            if self.point_of_interests[poi].used_in_search:
                lat_total += self.point_of_interests[poi].latitude
                lon_total += self.point_of_interests[poi].longitude
        self.central_point = truncate_coords(lat_total / number_of_locations) + \
                             ',' + truncate_coords(lon_total / number_of_locations)