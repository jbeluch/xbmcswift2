import os
import pickle
from xbmcswift2.storage import _Storage, TimedStorage
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
        storage = _Storage(filename, file_format='pickle')

        storage['name'] = 'jon'
        storage.update({'answer': 42})
        storage.close()

        storage2 = _Storage(filename, file_format='pickle')
        self.assertEqual(storage, storage2)
        self.assertEqual(2, len(storage2.items()))
        self.assertTrue('name' in storage2.keys())
        self.assertTrue('answer' in storage2.keys())
        self.assertEqual('jon', storage2.pop('name'))
        self.assertEqual(42, storage2['answer'])

        remove(filename)
        
    def test_csv(self):
        filename = '/tmp/testdict.csv'
        remove(filename)
        storage = _Storage(filename, file_format='csv')

        storage['name'] = 'jon'
        storage.update({'answer': '42'})
        storage.close()

        storage2 = _Storage(filename, file_format='csv')
        self.assertEqual(sorted(storage.items()), sorted(storage2.items()))
        self.assertEqual(2, len(storage2.items()))
        self.assertTrue('name' in storage2.keys())
        self.assertTrue('answer' in storage2.keys())
        self.assertEqual('jon', storage2.pop('name'))
        self.assertEqual('42', storage2['answer'])

        remove(filename)
    
    def test_json(self):
        filename = '/tmp/testdict.json'
        remove(filename)
        storage = _Storage(filename, file_format='json')

        storage['name'] = 'jon'
        storage.update({'answer': '42'})
        storage.close()

        storage2 = _Storage(filename, file_format='json')
        self.assertEqual(sorted(storage.items()), sorted(storage2.items()))
        self.assertEqual(2, len(storage2.items()))
        self.assertTrue('name' in storage2.keys())
        self.assertTrue('answer' in storage2.keys())
        self.assertEqual('jon', storage2.pop('name'))
        self.assertEqual('42', storage2['answer'])

        remove(filename)
    

class TestTimedStorage(TestCase):
    def test_pickle(self):
        filename = '/tmp/testdict.pickle'
        remove(filename)
        storage = TimedStorage(filename, file_format='pickle', TTL=timedelta(hours=1))
        storage['name'] = 'jon'
        storage.update({'answer': 42})
        storage.close()

        # Reopen
        storage2 = TimedStorage(filename, file_format='pickle', TTL=timedelta(hours=1))
        self.assertEqual(sorted(storage.items()), sorted(storage2.items()))

        # Reopen again but with a one second TTL which will be expired
        time.sleep(2)
        storage3 = TimedStorage(filename, file_format='pickle', TTL=timedelta(seconds=1))
        self.assertEqual([], sorted(storage3.items()))
        storage3.close()

        # Ensure the expired dict was synced
        storage4 = TimedStorage(filename, file_format='pickle', TTL=timedelta(hours=1))
        self.assertEqual(sorted(storage3.items()), sorted(storage4.items()))
