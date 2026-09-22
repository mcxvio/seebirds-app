""" Tests for eBird API """
import sys
import unittest
import json
import ijson

#sys.path.insert(0, '/tests')
#sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3_api/apis')
#print(sys.path)

from time import gmtime, strftime
from apis.ebird import requester
from apis.ebird import service
from apis.ebird import reformat

class EbirdApiMethods(unittest.TestCase):

    def test_get_ebird_key(self):
        """ Get the eBird key for API 2.0 """
        data = ''
        with open('keys.json') as json_data_file:
            data = json.load(json_data_file)
        print('\n')
        print("test_get_ebird_key: ", str(data['ebird_key']))
        self.assertGreater(len(data), 0)

    def test_valid_region_for_obs(self):
        """ Valid region for a region observation, 2.0 API """
        response = service.region_checklists('US-MA-025')
        print("test_valid_region_for_obs response: ", len(response))
        self.assertGreater(len(response), 0)

    def test_valid_region_for_species(self):
        """ Valid region for a region species observation? """
        response = service.region_species_code_obs('GB-SCT', 'hoocro1', '5') # hooded crow in Scotland
        print("test_valid_region_for_species response: ", len(response))
        self.assertGreater(len(response), 0)

    def test_extract_type_from_region(self):
        """ Extract region type from selected region """
        result = reformat.extract_region_code('Suffolk (US-MA-025)')
        self.assertEqual(result, 'US-MA-025')

    def test_extract_sub_from_sub_code(self):
        """ Extract subregion from a subregion code (fix bug) """
        result = reformat.extract_region_code('US-MA-025')
        self.assertEqual(result, 'US-MA-025')

    def test_region_is_country(self):
        """ Region is a country? """
        result = reformat.extract_region_type('US-')
        self.assertEqual(result, 'country')

    def test_region_is_state(self):
        """ Region is a state? """
        result = reformat.extract_region_type('US-MA')
        self.assertEqual(result, 'subnational1')

    def test_region_is_county(self):
        """ Region is a county? """
        result = reformat.extract_region_type('US-MA-025')
        self.assertEqual(result, 'subnational2')

    # Invalid data tests
    def test_invalid_region_for_obs(self):
        """ Invalid region for a region observation? """
        response = service.region_checklists('XX-XX-000')
        print("test_invalid_region_obs response: ", response)
        self.assertEqual(str(response), '[]')

    def test_invalid_region_for_notable(self):
        """ Invalid region for a region notable observation? """
        response = service.region_notable('subregion', '5')
        print("test_invalid_region_notable response: ", response)
        self.assertIsNone(response)

    def test_invalid_region_for_species_obs(self):
        """ Invalid region for a region species observation? """
        response = service.region_species_code_obs('subregion', 'rocpig1', '5')
        print("test_invalid_region_species_obs response: ", response)
        self.assertIsNone(response)

    def test_invalid_hotspot_for_obs(self):
        """ Invalid hotspot for a hotspot observation? """
        response = service.region_hotspots('LocX')
        print("test_invalid_hotspot_obs response: ", response)
        self.assertIn('errors', str(response))

    def test_invalid_spp_for_species(self):
        """ Invalid species for a region species observation? """
        response = service.region_species_code_obs('US-MA-025', 'Sci name', '5')
        print("test_invalid_spp_for_species response: ", response)
        self.assertIsNone(response)

    def test_invalid_regspp_for_regspp(self):
        """ Invalid region and species for region species observation? """
        response = service.region_species_code_obs('subnational', 'Sci name', '5')
        print("test_invalid_region_species_obs response: ", response)
        self.assertIsNone(response)

    def test_datetime_format_options(self):
        """" Datetime returned when passing datetime and format parameter """
        dateortime = 'da'
        value = "2017-11-21 17:07"
        response = reformat.extract_date_time(value, dateortime)
        self.assertEqual(response, "Tuesday 21 November")

    if __name__ == '__main__':
        unittest.main()
