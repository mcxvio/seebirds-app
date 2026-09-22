""" Tests Flask-Session data store.
    TODO-get these tests working with their own context."""
import sys
import unittest
from flask import session

#sys.path.insert(1, '/home/mrhapi/murmuration')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3/apis')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3/persistence')

print(sys.path)

class FlaskSessionTestCase(unittest.TestCase):
    """
    def setUp(self):
    def tearDown(self):
    """

    def test_save_previous_region(self):
        """ Save to flask session. """
        region = "Suffolk (US-MA-025)"
        region_code = region[region.find("(")+1:region.find(")")]
        session[region_code] = region
        self.assertEqual(session, None)

    def test_get_previous_regions(self):
        """ Retrieve from flask session. """
        data = []
        for key in session:
            data.append(session[key])
        self.assertEqual(data, None)

    def clear_previous_regions(self):
        """ Clear previously searched for terms. """
        session.clear()
        self.assertEqual(len(session.keys()), 0)

    if __name__ == '__main__':
        unittest.main()