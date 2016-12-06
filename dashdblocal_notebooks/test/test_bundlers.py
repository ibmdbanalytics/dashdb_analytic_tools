#!/usr/bin/env python3

import sys, subprocess
import tornado.web
import unittest
import unittest.mock as mock

import jupyter_cms_sparkapp.sparkapp_upload as upload


TEST_NOTEBOOK = "/test/TestNotebook.ipynb"
#TEST_NOTEBOOK = "/home/jovyan/work/Spark_KMeansSample.ipynb"

class TestSparkappBundler(unittest.TestCase):

    def setUp(self):
        self.handler_output = ""

    def handlerWrite(self, text):
        print(text, end='')
        if (isinstance(text, bytes)):
            self.handler_output += text.decode('UTF-8')
        else:
            self.handler_output += text

    def testSparkappUpload(self):
        print("Testing SparkApp upload")
        handler = mock.create_autospec(tornado.web.RequestHandler)
        # overwrite the write implementation of the mock. note: self.handlerWrite is a bound
        # method, so "self" inside handlerWrite refers to the testcase, not the handler
        handler.write = self.handlerWrite

        submit_commands = upload.bundle(handler, TEST_NOTEBOOK).result()
        self.assertIn("Successfully uploaded TestNotebook", self.handler_output)
        self.assertIn("spark-submit", submit_commands[-1])
        
        submit_line = " && ".join(submit_commands)
        print("Submitting uploaded application as\n\t{0}".format(submit_line))
        submit_output_bin = subprocess.check_output(submit_line, shell=True)
        submit_output = submit_output_bin.decode()
        print (submit_output)
        self.assertIn("Status: submitted", submit_output)


if __name__ == '__main__':
    unittest.main()
