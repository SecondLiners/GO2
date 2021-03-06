#
# tests for band object
#

import unittest
import webapp2
import main
import band
from google.appengine.ext import ndb

from google.appengine.ext import testbed


class BandTestCase(unittest.TestCase):

    # Needed to get webapp2 to use a WSGIApplication application instance,
    # which is easier to configure in setUp().
    webapp2._local = None

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        # Need to set up a global application and Request instance for
        # the i18n module to work. There's probably a more elegant way
        # of doing this.
        self.request_stub = webapp2.Request.blank("/")
        self.request_stub.user = None
        self.request_stub.app = main.APPLICATION
        webapp2.WSGIApplication.app = main.APPLICATION
        webapp2.get_app().set_globals(main.APPLICATION, self.request_stub)

    def tearDown(self):
        self.testbed.deactivate()

    def assertNotEmpty(self, obj):
        self.assertTrue(obj is not None and len(obj) > 0)

    def _make_test_band(self):
        return band.new_band("test band")

    def test_new_band(self):
        the_band = self._make_test_band()
        self.assertIsNotNone(the_band)
        self.assertTrue(isinstance(the_band, band.Band))

        # demonstrate we can get
        check_band = band.get_band(the_band.key)
        self.assertEqual(check_band.name, "test band")

        # demonstrate we can put
        check_band.name = "band testing"
        band.put_band(check_band)

        check2 = band.get_band(the_band.key)
        self.assertEqual(check2.name, "band testing")

    def test_delete_band(self):
        self._make_test_band()

        all_band_keys = band.get_all_bands(keys_only=True)
        self.assertNotEmpty(all_band_keys)
        self.assertEqual(len(all_band_keys), 1)
        self.assertTrue(isinstance(all_band_keys[0], ndb.Key))

        band.forget_band_from_key(all_band_keys[0])
        all_band_keys = band.get_all_bands(keys_only=True)
        self.assertTrue(len(all_band_keys)==0)

    def test_band_from_urlsafe(self):
        the_band = self._make_test_band()
        other_band_key = band.band_key_from_urlsafe(the_band.key.urlsafe())
        self.assertEqual(the_band.key, other_band_key)

    def test_band_from_name(self):
        the_band = self._make_test_band()
        other_band = band.get_band_from_condensed_name(the_band.condensed_name)
        self.assertEqual(the_band.key, other_band.key)

    def test_band_sections(self):
        the_band = self._make_test_band()
        section_keys = band.get_section_keys_of_band_key(the_band.key)
        self.assertEqual(len(section_keys), 0)

        band.new_section_for_band(the_band, "section1")
        band.new_section_for_band(the_band, "section2")

        section_keys = band.get_section_keys_of_band_key(the_band.key)
        self.assertEqual(len(section_keys), 2)
        sections = band.get_sections_from_keys(section_keys)
        self.assertEqual(len(sections), 2)

        band.delete_section_key(section_keys[1])
        section_keys = band.get_section_keys_of_band_key(the_band.key)
        self.assertEqual(len(section_keys), 1)

        band.delete_section_key(section_keys[0])
        section_keys = band.get_section_keys_of_band_key(the_band.key)
        self.assertEqual(len(section_keys), 0)

        # todo add tests that show that members who are using a section are
        # reverted to 'None' section when that section is deletec


    def test_band_api(self):
        the_band = self._make_test_band()
        the_info = band.rest_band_info(the_band)
        for x in ['plan_feedback', 'simple_planning', 'description', 'shortname', 'sections', 'name']:
            tval = the_info[x] if the_info[x] else None
            bval = getattr(the_band, x)
            if not bval:
                bval = None
            self.assertEqual(tval, bval)
        self.assertEqual(the_info['id'], the_band.key.urlsafe())

if __name__ == '__main__':
    unittest.main()