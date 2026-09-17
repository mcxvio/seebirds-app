"""
Main entry to application.
"""
from apis.ebird import service
from apis.ebird import reformat
from apis.ebird import history as searches
import ijson
import time
from flask import Flask
from flask import render_template
from flask import redirect
# session management
from flask import session
from flask_session import Session

app = Flask(__name__, static_folder='', static_url_path='')
app.config.from_pyfile('app.cfg')
app.secret_key = app.config['SECRET_KEY']

@app.route('/', methods=['GET'])
def index():
    """ Show index page. """
    return render_template('home.html')

@app.route('/clear', methods=['GET'])
def clear():
    """ Clear previous region searches. """
    searches.clear_previous_regions()
    return redirect("/")

# checklists
@app.route('/checklists', methods=['GET'])
def get_checklist_search():
    """ Show checklist search page. """
    previous = searches.get_previous_regions()
    return render_template('checklists_find.html', previous=previous, page="checklists")

@app.route('/checklists/<string:region>', methods=['GET'])
def get_checklists(region):
    """ Show checklist search results. """
    searches.save_previous_region(region)
    data = service.region_checklists(region)
    return render_template('checklists_results.html', data=data, region=region)

@app.route('/checklists/<string:region>/<path:location_name>/<string:location_id>', methods=['GET'])
def get_checklists_location(region, location_name, location_id):
    """ Show location's recent checklists results. """
    #searches.save_previous_region(region)
    days = str(app.config['DAYS_BACK'])
    data = service.region_checklists(location_id)
    return render_template('checklists_location_results.html', data=data, region=region, days=days, name=location_name, id=location_id)

# submission
@app.route('/submission/<string:region>/<path:location_name>/<string:submission_id>', methods=['GET'])
def get_checklist_submission(region, location_name, submission_id):
    """ Show checklist submission details. """
    data = service.checklist_submission(submission_id)
    return render_template('submission_results.html', data=data, region=region, location_name=location_name)

# notables
@app.route('/notables', methods=['GET'])
def get_notables_search():
    """ Show notables search page. """
    previous = searches.get_previous_regions()
    return render_template('notables_find.html', previous=previous, page="notables")

@app.route('/notables/<string:region>', methods=['GET'])
def get_notables(region):
    """ Show notable search results. """
    searches.save_previous_region(region)
    days = str(app.config['DAYS_BACK'])
    data = service.region_notable(region, days)
    return render_template('notables_results.html', data=data, region=region, days=days)

# locations
@app.route('/locations/<string:region>/<path:location_name>/<string:location_id>', methods=['GET'])
def get_species_by_location(region, location_name, location_id):
    """ Show location species page. """
    searches.save_previous_hotspots(region, location_name, location_id)
    days = str(app.config['DAYS_BACK'])
    data = service.region_location_obs(location_id, days)
    return render_template('locations_results.html', data=data, region=region, name=location_name, id=location_id, days=days)

# species
@app.route('/species/<string:region>/<path:full_name>', methods=['GET'])
def get_species_by_region(region, full_name):
    """ Show species page. """
    days = str(app.config['DAYS_BACK'])
    searches.save_previous_region(region)
    data = service.region_species_code_obs(region, full_name, days)
    return render_template('species_results.html', data=data, region=region, name=full_name, days=days)

# hotspots
@app.route('/hotspots', methods=['GET'])
def get_hotspots_search():
    """ Show hotspots search page. """
    previous = searches.get_previous_regions()
    return render_template('hotspots_find.html', previous=previous, page="hotspots")

@app.route('/hotspots/<string:region>', methods=['GET'])
def get_hotspots(region):
    """ Show hotspots results page. """
    searches.save_previous_region(region)
    previous = searches.get_previous_hotspots(region)
    return render_template('hotspots_results.html', previous=previous, page="locations", region=region)

@app.route('/hotspots/all/<string:region>', methods=['GET'])
def get_hotspots_all(region):
    """ Show hotspots results page for all hotspots in a region. """
    data = service.region_hotspots(region)
    return render_template('hotspots_results_all.html', data=data, page="hotspots", region=region)

# taxa
@app.route('/taxa', methods=['GET'])
def get_taxa_search():
    """ Show taxa search page. """
    previous = searches.get_previous_species()
    return render_template('taxa_find.html', previous=previous, page="taxa")

@app.route('/taxa/<string:species>/<string:family>/<string:order>', methods=['GET'])
def get_taxa(species, family, order):
    """ Show taxa results page. """
    previous = searches.get_previous_regions()
    searches.save_previous_species(species, family, order)
    name = species[0:species.rfind("(")]
    code = species[species.rfind("(")+1:species.rfind(")")]
    return render_template('taxa_results.html', name=name, code=code, family=family, order=order,
                           previous=previous, page="species")

# taxonomy
@app.route('/families/<string:family>', methods=['GET'])
def get_family_species(family):
    """ Show taxa family results page. """
    data = service.family_species(family)
    return render_template('taxa_results_family.html', data=data)

@app.route('/orders/<string:order>', methods=['GET'])
def get_order_species(order):
    """ Show taxa order results page. """
    data = service.order_species(order)
    return render_template('taxa_results_order.html', data=data)

@app.route('/extinct', methods=['GET'])
def get_extinct_species():
    """ View all the extinct species and year of extinction. """
    data = service.extinct_species_all()
    return render_template('extinct_results.html', data=data)

# data
@app.route('/data_taxaspecies', methods=['GET'])
def get_taxa_data():
    """ Return the species data from root, enabling both typeahead and json file searches. """
    return app.send_static_file('data_taxaspecies.json')

@app.route('/data_subnationals', methods=['GET'])
def get_region_data():
    """ Return the region data from root, for consistency with species data. """
    return app.send_static_file('data_subnationals2.json')

@app.route('/data_hotspots/<string:region>', methods=['GET'])
def get_hotspots_data(region):
    """ Show hotspots data for filter. """
    data = service.region_hotspots_all(region)
    return data

@app.route('/historic/<string:region_code>/<string:historic_date>', methods=['GET'])
def get_historic_data(region_code, historic_date):
    data = service.region_species_historic_obs(region_code, historic_date)
    return str(data)

# providers
@app.route('/providers', methods=['GET'])
def get_providers():
    """ Show providers/preferences page. """
    return render_template('providers.html')

#@app.route("/jasmine")
#def jasmine():
#    """ Show test page. """
#    return app.send_static_file('tests/jasmine/SpecRunner.html')


if __name__ == '__main__':
    app.run(debug=True)