""" Tests for eBird API """
import sys
import unittest
import json
import ijson

class EbirdJsonMethods(unittest.TestCase):

    def test_extinct_species_from_json(self):
        """ View all the extinct species and year of extinction. """
        response = []
        with open('data_taxaspecies.json', 'rb') as json_data_file:
            data = ijson.items(json_data_file, 'response.taxa.item')
            species = (s for s in data if s.get('extinct') is not None and s['extinct'])
            response = list(species)
        self.assertGreater(len(response), 0)

    def test_family_species_from_json(self):
        """ Valid family name to retrieve species. """
        response = ""
        with open('data_taxaspecies.json', 'rb') as json_data_file:
            data = ijson.items(json_data_file, 'response.taxa.item')
            species = (s for s in data if s.get("familyComName") is not None
                       and s["familyComName"] == 'Ostriches')
            response = list(species)
        self.assertGreater(len(response), 0)

    def test_familysciname_species_from_stream(self):
        """ Valid family name to retrieve species via stream. """
        stream = []
        species = ""
        family = ""
        familySciName = "Struthionidae"
        with open('data_taxaspecies.json', 'rb') as json_data_file:

            parser = ijson.parse(json_data_file)
            for prefix, event, value in parser:
                if (prefix, event) == ('response.taxa.item.comName', 'string'):
                    species = value
                elif (prefix, event) == ('response.taxa.item.familyComName', 'string'):
                    family = value
                elif (prefix, event) == ('response.taxa.item.familySciName', 'string') and value == familySciName:
                    stream.append('%s' % species + '--' + family + '--' + familySciName)
                    species = ""
                    family = ""
                elif (prefix, event) == ('response.taxa.item.familySciName', 'string') and value != familySciName and len(stream) > 0:
                    break
        print(*stream, sep = '\n')
        self.assertGreater(len(stream), 0)

    def test_family_species_from_stream(self):
        """ Valid family name to retrieve species via stream. """
        stream = []
        species = ""
        order = ""
        family = "Ostriches"
        with open('data_taxaspecies.json', 'rb') as json_data_file:

            parser = ijson.parse(json_data_file)
            for prefix, event, value in parser:
                if (prefix, event) == ('response.taxa.item.comName', 'string'):
                    species = value
                elif (prefix, event) == ('response.taxa.item.order', 'string'):
                    order = value
                elif (prefix, event) == ('response.taxa.item.familyComName', 'string') and value == family:
                    stream.append('%s' % species + '_' + value + '_' + order)
                    species = ""
                    order = ""
                elif (prefix, event) == ('response.taxa.item.familyComName', 'string') and value != family and len(stream) > 0:
                    break
        print(*stream, sep = '\n')
        self.assertGreater(len(stream), 0)

    if __name__ == '__main__':
        unittest.main()