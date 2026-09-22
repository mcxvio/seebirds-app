"""
Return previous searches from repository.
"""
#from persistence import redis_instance as connection
from flask import session

# regions
def save_previous_region(region):
    """ Try to save to redis or default to flask session. """
    region_code = region[region.find("(")+1:region.find(")")]
    #if connection.get_connection() != None:
    #    connection.save_key_value(region_code, region)
    #else:
    session[region_code] = "r:" + region

def get_previous_regions():
    """ Try to retrieve from redis or default to flask session. """
    #if connection.get_connection() != None:
    #    return connection.get_values()
    #else:
    data = []
    for key in session:
        if 'r:' in session[key]:
            data.append(session[key][2:].replace("%20", " "))
    return data

def clear_previous_regions():
    """ Clear previously searched for terms. """
    #if connection.get_connection() != None:
    #    connection.clear_values()
    #else:
    session.clear()

# species
def save_previous_species(species, family, order):
    """ Save species to flask session. """
    species_code = species[species.rfind("(")+1:species.rfind(")")]
    session[species_code] = "s:" + species + "/" + family + "/" + order

def get_previous_species():
    """ Retrieve species from flask session. """
    data = []
    for key in session:
        if 's:' in session[key]:
            data.append(session[key][2:].replace("%20", " "))
    return data

def clear_previous_species():
    """ Clear previously searched for terms. """
    session.clear()

# hotspots
def save_previous_hotspots(region, location_name, location_id):
    """ Save region & hotspot to flask session. """
    session[location_id] = "h:" + region + "/" + location_name + "/" + location_id

def get_previous_hotspots(region):
    """ Retrieve region & hotspot from flask session. """
    data = []
    for key in session:
        if 'h:' in session[key]:
            if region in session[key]:
                data.append(session[key][2:].replace("%20", " "))
    return data

def clear_previous_hotspots():
    """ Clear previously searched for terms. """
    session.clear()