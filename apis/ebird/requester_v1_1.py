"""
Query eBird 1.1 API.
"""
import requests

def region_obs(rtype, subregion):
    """ checklists """
    response = requests.get("http://ebird.org/ws1.1/data/obs/region/recent?rtype="
                            + rtype + "&r="
                            + subregion
                            + "&hotspot=true&includeProvisional=true&back=5&fmt=json")

    if response.status_code == 400:
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    else:
        assert response.status_code == 200

    return response.text

def region_notable(rtype, subregion):
    """ notables """
    response = requests.get("http://ebird.org/ws1.1/data/notable/region/recent?rtype="
                            + rtype + "&r="
                            + subregion
                            + "&detail=full&hotspot=true&back=5&fmt=json")

    if response.status_code == 400:
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    else:
        assert response.status_code == 200

    return response.text

def hotspot_obs(location_id):
    """ locations """
    response = requests.get("http://ebird.org/ws1.1/data/obs/hotspot/recent?r="
                            + location_id
                            + "&detail=full&includeProvisional=true&back=10&fmt=json")

    if response.status_code == 400:
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    else:
        assert response.status_code == 200

    return response.text

def region_species_obs(rtype, subregion, sci_name):
    """ species """
    response = requests.get("http://ebird.org/ws1.1/data/obs/region_spp/recent?rtype="
                            + rtype + "&r="
                            + subregion + "&sci="
                            + sci_name + "&hotspot=true&includeProvisional=true&back=10&fmt=json")

    if response.status_code == 400:
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    else:
        assert response.status_code == 200

    return response.text
