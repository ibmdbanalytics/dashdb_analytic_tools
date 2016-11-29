#!/usr/bin/env python2

import sys, os, re, requests
import unittest
from urlparse import urljoin
# python3
#from urllib.parse import urljoin


DASHDBHOST = os.environ.get('DASHDBHOST')
DASHDBUSER = os.environ.get('DASHDBUSER')
DASHDBPASS = os.environ.get('DASHDBPASS')
if (not DASHDBUSER or not DASHDBPASS or not DASHDBHOST): sys.exit("DASHDBUSER, DASHDBPASS and DASHDBHOST variables must be defined")


class TestNotebookUI(unittest.TestCase):

    def setUp(self):
        self.sess = requests.Session()

    def tearDown(self):
        self.sess.close()

    def testUI(self):
        notebook_url = 'http://localhost:8888'
        print("Accesssing notebook at {0}".format(notebook_url))
        resp = self.sess.get(notebook_url)
        self.assertIn("Notebook server for {0}".format(DASHDBUSER, DASHDBHOST), resp.text)
        self.assertIn('<input type="password"', resp.text)
        match = re.search(r'<form action="([^"]+)"', resp.text)
        self.assertTrue(match)
        
        login_url = urljoin(resp.url, match.group(1))
        login_params = { 'password': DASHDBPASS }
        resp = self.sess.post(login_url, data=login_params)
        self.assertIn('<button id="logout"', resp.text)

if __name__ == '__main__':
    unittest.main()
