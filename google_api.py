import requests
import configs
import place

# add error checks

def point_of_interest_search(poi):
    """
    Calls a GET HTTP request to Google's place search api 
    and grabs the JSON of the point of interest.

    :poi: point of interest search
        :type: str

    :return: point of interest 
        :type: PointOfInterest object
    """
    url = configs.get_api_url(configs.GOOGLE_CONFIGS) + \
          configs.get_api_path(configs.GOOGLE_CONFIGS, 'placeSearch')
    params = {'key': configs.get_api_key(configs.GOOGLE_CONFIGS), 
              'input': poi.replace(' ', '%20'), 
              'inputtype': 'textquery',
              'fields': 'place_id,formatted_address,geometry,name'}
    response = requests.get(url, params)

    #error check when response status != 200

    json = response.json()
    return place.PointOfInterest(json['candidates'][0]['name'],
                                 json['candidates'][0]['place_id'],
                                 json['candidates'][0]['geometry']['location']['lat'],
                                 json['candidates'][0]['geometry']['location']['lng'],
                                 json['candidates'][0]['formatted_address'])

def lodging_search(central_point, lodging_type, radius, page_token):
    """
    Calls a GET HTTP request to Google's text search request api. 
    Adds the found lodging informations to the search list.

    :central_point: location in latitude and longitude
        :type: str
    
    :lodging_type: hotel or hostel; user's lodging search type
        :type: str

    :radius: max distance, in meters, away from central point to find lodgings
        :type: int

    :page_token: searches additional results from previous parameters
        :Note: only available if there was a previous search and more results
        :type: str

    :return: list of Lodgings and next page token if available
        :type: [Lodging objects], str
    """
    url = configs.get_api_url(configs.GOOGLE_CONFIGS) + \
          configs.get_api_path(configs.GOOGLE_CONFIGS, 'placeNearbySearch')
    params = {'key': configs.get_api_key(configs.GOOGLE_CONFIGS)}
    if page_token:
        params['pagetoken'] = page_token
    else:
        params['location'] = central_point 
        params['keyword'] = lodging_type
        params['type'] = 'lodging'
        params['radius'] = radius
    response = requests.get(url, params)

    #error check when response status != 200

    json = response.json()
    results = []
    for i in json['results']:
        if i['business_status'] == 'OPERATIONAL':
            results.append(place.Lodging(i['name'], i['place_id'], 
                                         i['geometry']['location']['lat'],
                                         i['geometry']['location']['lng'], 
                                         i['vicinity'], i['rating'],
                                         i['user_ratings_total']))
    return results, json['next_page_token'] if 'next_page_token' in json else None