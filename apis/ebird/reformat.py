""" Reformat functions. """
from datetime import datetime

def blank_recurring_dates(response, dateortime):
    """ Show date the first time it occurs, blank otherwise. """
    previous_date = ""

    for item in response:
        obsDt = item['obsDt']
        if obsDt == previous_date:
            item['obsDt'] = ""
        else:
            previous_date = obsDt
            if dateortime != "":
                item['obsDt'] = extract_date_time(obsDt, dateortime)
           
    return response

def extract_hotspots(response):
    """ Extract hotspots...hopefully to be implemented by ebird. """
    hotspots = []
    for item in response:
        if item['loc']['isHotspot'] is True:
            hotspots.append(item)
            if len(hotspots) == 10:
                break
    return hotspots

def extract_date_time(value, dateortime):
    """ Extract date time. """
    if value[-4:-2] == "20": #eBird v2 date format.
        obs_date_time = datetime.strptime(value, '%d %b %Y')
    elif len(value) == 10:
        obs_date_time = datetime.strptime(value, '%Y-%m-%d')
    else:
        obs_date_time = datetime.strptime(value, '%Y-%m-%d %H:%M')

    if dateortime == 'dt':
        return obs_date_time.strftime('%d-%b, %Y, %H:%M')
    elif dateortime == 'da':
        return obs_date_time.strftime('%A %d %B')
    elif dateortime == 'd':
        return obs_date_time.strftime('%d %B')
    elif dateortime == 'dx':
        return obs_date_time.strftime('%Y-%m-%d')
    elif dateortime == 'ddt':
        return obs_date_time.strftime('%A %d %B, %H:%M')
    # 't' is the default option.
    return obs_date_time.strftime('%H:%M')

def extract_unique_date_times(response):
    """ Extract unique date time. """
    unique_dates = []
    for item in response:
        if not item['obsDt'] in unique_dates:
            unique_dates.append(item['obsDt'])
    return unique_dates

def extract_unique_dates(response):
    """ Extract unique dates. """
    unique_dates = []
    for item in response:
        if not extract_date_time(item['obsDt'], 'dx') in unique_dates:
            unique_dates.append(extract_date_time(item['obsDt'], 'dx'))
    return unique_dates

def extract_unique_submissions(response):
    """ Extract unique submissions (de-dup for submission per photograph). """
    unique_subs = []
    for item in response:
        if not item in unique_subs:
            unique_subs.append(item)
    return unique_subs

def remove_ob_items(observation):
    """ Remove observation items. """
    del observation['sciName']
    del observation['comName']
    #del ob['howMany']
    del observation['obsValid']
    del observation['obsReviewed']
    #return ob

def add_checklists_for_date(add_date, checklists, submission, submissions):
    """ Add checklists for date. """
    submission['obsDt'] = add_date
    submission['checklists'] = checklists
    submissions.append(submission)

def extract_region_code(region):
    """ Extract the region between the brackets in the selected region name. """
    if region.find("(") > 0: #Check for brackets.
        region_code = region[region.find("(")+1:region.find(")")]
        return region_code

    return region #Pass-through.

def extract_scientific_name(full_name):
    """ Extract scientific name. """
    if full_name.find("(") > 0: #Check for brackets.
        sci_name = full_name[full_name.find("(")+1:full_name.find(")")]
        return sci_name

    return full_name #Pass-through.

def extract_text_between_brackets(text):
    """ Extract scientific name. """
    if text.find("(") > 0: #Check for brackets.
        text_between = text[text.find("(")+1:text.find(")")]
        return text_between

    return text #Pass-through.

def extract_region_type(subregion):
    """ Count the separating dashes of the region code. """
    if len(subregion) == 3:
        subregion = subregion[0:2] #"US-" to "US".
        return "country"
    elif subregion.count("-") == 2:
        return "subnational2"

    return "subnational1"
