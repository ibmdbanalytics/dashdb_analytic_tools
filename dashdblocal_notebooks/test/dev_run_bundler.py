#!/usr/bin/env python3

import sys, subprocess
import tornado.web
import unittest
import unittest.mock as mock

import jupyter_cms_sparkapp.scalafile_download as download
import jupyter_cms_sparkapp.sparkapp_upload as upload


TEST_NOTEBOOK = "/test/TestNotebook.ipynb"

class TestSparkappBundler(unittest.TestCase):

    def setUp(self):
        self.handler_output = ""

    def handlerWrite(self, text):
        print(text, end='')
        if (isinstance(text, bytes)):
            self.handler_output += text.decode('UTF-8')
        else:
            self.handler_output += text

    def testBundler(self):
        print("Testing")
        handler = mock.create_autospec(tornado.web.RequestHandler)
        handler.write = self.handlerWrite

        download.bundle(handler, TEST_NOTEBOOK)
        #upload.bundle(handler, TEST_NOTEBOOK)
        #print(self.handler_output)

if __name__ == '__main__':
    unittest.main()
