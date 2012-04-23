import os
import pickle
from xbmcswift2.cache import Cache, TimedCache
from unittest import TestCase
from datetime import timedelta
import time


def remove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


class TestCache(TestCase):

    def test_pickle(self):
        filename = '/tmp/testdict.pickle'
        remove(filename)
        cache = Cache(filename, file_format='pickle')

        cache['name'] = 'jon'
        cache.update({'answer': 42})
        cache.close()

        cache2 = Cache(filename, file_format='pickle')
        self.assertEqual(cache, cache2)
        self.assertEqual(2, len(cache2.items()))
        self.assertTrue('name' in cache2.keys())
        self.assertTrue('answer' in cache2.keys())
        self.assertEqual('jon', cache2.pop('name'))
        self.assertEqual(42, cache2['answer'])

        remove(filename)
        
    def test_csv(self):
        filename = '/tmp/testdict.csv'
        remove(filename)
        cache = Cache(filename, file_format='csv')

        cache['name'] = 'jon'
        cache.update({'answer': '42'})
        cache.close()

        cache2 = Cache(filename, file_format='csv')
        self.assertEqual(sorted(cache.items()), sorted(cache2.items()))
        self.assertEqual(2, len(cache2.items()))
        self.assertTrue('name' in cache2.keys())
        self.assertTrue('answer' in cache2.keys())
        self.assertEqual('jon', cache2.pop('name'))
        self.assertEqual('42', cache2['answer'])

        remove(filename)
    
    def test_json(self):
        filename = '/tmp/testdict.json'
        remove(filename)
        cache = Cache(filename, file_format='json')

        cache['name'] = 'jon'
        cache.update({'answer': '42'})
        cache.close()

        cache2 = Cache(filename, file_format='json')
        self.assertEqual(sorted(cache.items()), sorted(cache2.items()))
        self.assertEqual(2, len(cache2.items()))
        self.assertTrue('name' in cache2.keys())
        self.assertTrue('answer' in cache2.keys())
        self.assertEqual('jon', cache2.pop('name'))
        self.assertEqual('42', cache2['answer'])

        remove(filename)
    

class TestTimedCache(TestCase):
    def test_pickle(self):
        filename = '/tmp/testdict.pickle'
        remove(filename)
        cache = TimedCache(filename, file_format='pickle', ttl=timedelta(hours=1))
        cache['name'] = 'jon'
        cache.update({'answer': 42})
        cache.close()

        # Reopen
        cache2 = TimedCache(filename, file_format='pickle', ttl=timedelta(hours=1))
        self.assertEqual(sorted(cache.items()), sorted(cache2.items()))

        # Reopen again but with a one second ttl which will be expired
        time.sleep(2)
        cache3 = TimedCache(filename, file_format='pickle', ttl=timedelta(seconds=1))
        self.assertEqual([], sorted(cache3.items()))
        cache3.close()

        # Ensure the expired dict was synced
        cache4 = TimedCache(filename, file_format='pickle', ttl=timedelta(hours=1))
        self.assertEqual(sorted(cache3.items()), sorted(cache4.items()))
