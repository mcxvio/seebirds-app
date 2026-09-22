"""
Query eBird 2.0 API.
"""
import json
import requests

def get_ebird_key():
    """ Get the eBird key for API 2.0 """
    with open('keys.json') as json_data_file:
        data = json.load(json_data_file)
    return data['ebird_key']

def region_checklists(region_code):
    """ recent checklists """
    response = requests.get("https://ebird.org/ws2.0/product/lists/"
                            + region_code
                            + "?maxResults=20",
                            headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def checklist_submission(submission_id):
    """ checklist details """
    #https://ebird.org/ws2.0/product/checklist/view/{{subId}}
    response = requests.get("https://ebird.org/ws2.0/product/checklist/view/"
                            + submission_id,
                            headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def species_common_name(species_code):
    """ checklist details """
    #https://ebird.org/ws2.0/product/checklist/view/{{subId}}
    response = requests.get("https://ebird.org/ws2.0/ref/taxonomy/ebird?species="
                            + species_code
                            + "&fmt=json",
                            headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def region_notable(region_code, days):
    """ notables """
    response = requests.get("https://ebird.org/ws2.0/data/obs/"
                            + region_code
                            + "/recent/notable"
                            + "?&detail=full"
                            + "&hotspot=true"
                            + "&back=" + days,
                            headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def region_species_obs(region_code, species_code, days):
    """ species """
    response = requests.get("https://ebird.org/ws2.0/data/obs/"
                            + region_code
                            + "/recent/"
                            + species_code
                            + "?hotspot=true"
                            + "&includeProvisional=true"
                            + "&back=" + days,
                            headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def region_species_historic_obs(region_code, historic_date):
    response = requests.get("https://ebird.org/ws2.0/data/obs/"
                        + region_code
                        + "/historic/"
                        + "2016/01/01"
                        + "?rank=mrec"
                        + "&detail=full"
                        + "&cat=species",
                        headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def region_location_obs(location_id, days):
    """ location/hotspot """
    response = requests.get("https://ebird.org/ws2.0/data/obs/"
                            + location_id
                            + "/recent"
                            + "?includeProvisional=true"
                            + "&back=" + days,
                            headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def region_hotspots(region_code):
    """ region hotspots """
    response = requests.get("https://ebird.org/ws2.0/ref/hotspot/"
                            + region_code
                            + "?fmt=json",
                            headers=get_ebird_key())
    handle_status_code(response)

    return response.text

def handle_status_code(response):
    """ Handle respose status codes """
    if response.status_code == 400:
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    elif response.status_code == 500:
        # API error.
        assert response.status_code == 500
    elif response.status_code == 503:
        # Forbidden, likely bad ebird key.
        assert response.status_code == 503
    else:
        assert response.status_code == 200
