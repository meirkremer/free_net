import unittest
from datetime import datetime

from db_client import *


class MyTestCase(unittest.TestCase):
    def test_check_user(self):
        print('a')
        insert_user('d', 'marworm1@gmail.com')
        result = check_user('marworm1@gmail.com')
        self.assertEqual(result, True)

    def test_delete_user(self):
        print('b')
        result = delete_user('marworm1@gmail.com')
        self.assertEqual(result, True)

    def test_insert_user(self):
        print('c')
        delete_user('marworm1@gmail.com')
        result = insert_user('meir', 'marworm1@gmail.com')
        self.assertEqual(result, True)
        result = insert_user('meir', 'marworm1@gmail.com')
        self.assertEqual(result, False)

    def test_insert_search(self):
        print('d')
        insert_user('meir', 'marworm1@gmail.com')
        result = insert_search('marworm1@gmail.com', 'some query', str(datetime.now()))
        self.assertEqual(result, True)

    def test_insert_download(self):
        print('e')
        insert_user('worm', 'marworm1@gmail.com')
        result = insert_download('marworm1@gmail.com', 'test name 44', 589764123087654, str(datetime.now()))
        self.assertEqual(result, True)

    def test_fetch_search(self):
        insert_user('s', 'marworm1@gmail.com')
        insert_search('marworm1@gmail.com', 'g', str(datetime.now()))
        result = fetch_search('marworm1@gmail.com')
        self.assertEqual(type(result), dict)

    def test_fetch_download(self):
        insert_user('s', 'marworm1@gmail.com')
        insert_download('marworm1@gmail.com', 'f', 589647233, str(datetime.now()))
        result = fetch_download('marworm1@gmail.com')
        self.assertEqual(type(result), dict)
