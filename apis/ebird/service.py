"""
Retrieve, format and return recent data.
"""
import json
import ijson

from apis.ebird import requester
from apis.ebird import reformat

def load_all_species_file():
    """ Load all species from json file to list. """
    species = []
    with open('data_taxaspecies.json') as json_data_file:
        taxa = ijson.items(json_data_file, 'response.taxa.item')
        species = list(s for s in taxa)
    return species

all_species = load_all_species_file()

def region_checklists(region):
    """ Latest 10 checklists submitted for the subregion. """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_checklists(region_code))
    response = reformat.extract_hotspots(response)
    response = reformat.blank_recurring_dates(response, 'da')
    return response

def location_checklists(location_id):
    """ Latest 10 checklists submitted for the location. """
    response = json.loads(requester.region_checklists(location_id))
    return response

def checklist_submission(submission_id):
    """ Checklist submission details. """
    response = json.loads(requester.checklist_submission(submission_id))

    response['obsTm'] = reformat.extract_date_time(response['obsDt'], 't')
    response['obsDt'] = reformat.extract_date_time(response['obsDt'], 'da')

    for obs in response["obs"]:
        for s in all_species: # pre-loaded class object.
            if obs['speciesCode'] == s['speciesCode']:
                obs['comName'] = s['comName']
                break

    return response

def region_notable(region, days):
    """ Notables """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_notable(region_code, days))
    response = reformat.extract_unique_submissions(response)
    # Handle invalid requests.
    if "errors" in str(response):
        return
    for item in response:
        item['obsTm'] = reformat.extract_date_time(item['obsDt'], 't')
        item['obsDt'] = reformat.extract_date_time(item['obsDt'], 'da')
    response = reformat.blank_recurring_dates(response, '') # Already formatted above.

    return response

def region_species_code_obs(region, full_name, days):
    """ Species """
    region_code = reformat.extract_region_code(region)
    if full_name.find("(") > 0:
        species_code = full_name[full_name.rfind("(")+1:full_name.rfind(")")]
    else:
        species_code = full_name
    response = json.loads(requester.region_species_obs(region_code, species_code, days))
    # Handle invalid requests.
    if "errors" in str(response):
        return
    for item in response:
        item['obsTm'] = reformat.extract_date_time(item['obsDt'], 't')
        item['obsDt'] = reformat.extract_date_time(item['obsDt'], 'da')
    response = reformat.blank_recurring_dates(response, '') # Already formatted above.

    return response

def region_species_obs(region, full_name, days):
    """ Species """
    region_code = reformat.extract_region_code(region)
    species_code = reformat.extract_text_between_brackets(full_name)
    response = json.loads(requester.region_species_obs(region_code, species_code, days))
    return response

def region_species_historic_obs(region_code, historic_date):
    response = json.loads(requester.region_species_historic_obs(region_code, historic_date.replace("-", "/")))
    return response

def region_location_obs(location_id, days):
    """ Location species """
    response = json.loads(requester.region_location_obs(location_id, days))
    if len(response) > 0:
        if ":" not in response[0]['obsDt']:
            response = reformat.blank_recurring_dates(response, 'da')
        else:
            response = reformat.blank_recurring_dates(response, 'ddt')
    return response

def region_hotspots(region):
    """ Hotspots """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_hotspots(region_code))
    return response

def region_hotspots_all(region):
    """ Hotspots """
    region_code = reformat.extract_region_code(region)
    return requester.region_hotspots(region_code)

def family_species(family):
    """ Family species """
    response = ""
    with open('data_taxaspecies.json') as json_data_file:
        data = ijson.items(json_data_file, 'response.taxa.item')
        species = (s for s in data if s.get("familyComName") is not None
                   and s["familyComName"] == family)

        response = list(species)
    return response

def order_species(order):
    """ Order species """
    response = ""
    with open('data_taxaspecies.json') as json_data_file:
        data = ijson.items(json_data_file, 'response.taxa.item')
        species = (s for s in data if s.get("order") is not None
                   and s["order"] == order)

        response = list(species)
    return response

def extinct_species_all():
    """ Extinct species. """
    response = ""
    with open('data_taxaspecies.json') as json_data_file:
        data = ijson.items(json_data_file, 'response.taxa.item')
        species = (s for s in data if s.get("extinct") is not None and s["extinct"])

        response = list(species)
    return response

def species_common_name(species_code):
    """ Species common name from species code. """
    data = requester.species_common_name(species_code)
    response = json.loads(data)[0]["comName"]
    return response