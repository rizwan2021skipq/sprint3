import pytest
import lambda_folder.mult_whp as ml
import urllib3
import datetime
import lambda_folder.url_retriever as urlr


def test_get_availability():
        """
        Test that an available website is actually available
        """
        url="https://www.skipq.org/"
        http = urllib3.PoolManager()
        result = ml.get_availability(url, http)
        assert result==1 
        

def test_pos_latency():
        """
        Test that latency is greater than zero
        """
        url="https://www.skipq.org/"
        http = urllib3.PoolManager()
        result = ml.get_latency(url, http)
        assert result> 0
        

'''
def test_url_list():
        """
        Test that latency is greater than zero
        """
        
        result = urlr.url_list()
        assert len(result)==4
'''
        
#if __name__ == '__main__':
#    unittest.main()