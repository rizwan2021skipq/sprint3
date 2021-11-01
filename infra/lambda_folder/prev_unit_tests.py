import unittest
import mult_whp as ml
import urllib3
import datetime
import url_retriever as urlr

class Test_availability(unittest.TestCase):
    def test_get_availability(self):
        """
        Test that an available website is actually available
        """
        url="https://www.skipq.org/"
        http = urllib3.PoolManager()
        result = ml.get_availability(url, http)
        self.assertEqual(result, 1)
        
class Test_latency(unittest.TestCase):
    def test_pos_latency(self):
        """
        Test that latency is greater than zero
        """
        url="https://www.skipq.org/"
        http = urllib3.PoolManager()
        result = ml.get_latency(url, http)
        self.assertGreater(result, 0)
        
class Test_url_list_func(unittest.TestCase):
    def test_url_list(self):
        """
        Test that latency is greater than zero
        """
        
        result = urlr.url_list()
        self.assertEquals(len(result), 4)
        
if __name__ == '__main__':
    unittest.main()