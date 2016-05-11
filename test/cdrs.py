# -*- coding: utf-8 -*-
import unittest

from versature.resources import Versature
from secrets import client_id, username, password, vendor_id

__author__ = 'DavidWard'


class CDRsTest(unittest.TestCase):

    def setUp(self):
        self.versature = Versature(username=username, password=password, client_id=client_id, vendor_id=vendor_id)


    ##################
    #### Get CDRs ####
    ##################

    def test_get_cdrs(self):
        result = self.versature.get_cdrs()
        self.assertIsNotNone(result)
