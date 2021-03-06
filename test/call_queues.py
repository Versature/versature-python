# -*- coding: utf-8 -*-
import sys
import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

import unittest
import time
from datetime import datetime, timedelta

from config import access_config
from config import reseller_config

from multiprocessing.dummy import Pool as ThreadPool

__author__ = 'DavidWard'


class CallQueuesTest(unittest.TestCase):

    def setUp(self):
        self.one_day_ago = datetime.utcnow() - timedelta(days=1)
        self.one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        self.today = datetime.utcnow()

    def test_call_queue_agents(self):
        result = access_config.call_center_supervisor.versature.call_queue_agents(queue=None)
        self.assertIsNotNone(result)

    #################################
    #### Login Call Queue Stats #####
    #################################

    def test_get_call_queues_stats(self):
        result = access_config.office_manager.versature.call_queue_stats(start_date=self.one_day_ago, end_date=self.today)
        self.assertIsNotNone(result)

    def test_get_call_queues_stats_multiple_requests(self):

        result = access_config.office_manager.versature.call_queue_stats(start_date=self.one_day_ago, end_date=self.today)
        self.assertIsNotNone(result)

        result = access_config.office_manager.versature.call_queue_stats(start_date=self.one_day_ago, end_date=self.today)
        self.assertIsNotNone(result)

    def test_get_call_queues_stats_cache_timeout(self):
        num_requests = 3
        pool = ThreadPool(num_requests)

        start_date = self.one_day_ago
        end_date = self.today

        def call_queue_test(*args, **kwargs):
            result = access_config.office_manager.versature.call_queue_stats(start_date=start_date, end_date=end_date)
            logging.debug("Call Queue Result: %s", result)

        result = pool.map(call_queue_test, range(num_requests))
        self.assertIsNotNone(result)

    def test_get_call_queues_stats_async(self):
        request = access_config.office_manager.versature.call_queue_stats(async=True, start_date=self.one_day_ago, end_date=self.today)
        result = request.resolve()
        self.assertIsNotNone(result)

    def test_call_queue_agents_inbound(self):
        result = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_day_ago, end_date=self.today,
                                                                               inbound=True, outbound=False, queue='8003')
        self.assertIsNotNone(result)

    def test_get_queue_agents_inbound(self):

        first_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_day_ago, end_date=self.today,
                                                                       inbound=True, outbound=False, queue='8814',
                                                                       cache_timeout=30)
        self.assertIsNotNone(first_response)

        time.sleep(30)

        second_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_day_ago, end_date=self.today,
                                                                       inbound=True, outbound=False, queue='8814',
                                                                       cache_timeout=30)
        self.assertIsNotNone(second_response)

    def test_expected_response_with_cache(self):
        expected_support_first_names = ['Andre', 'Jonathon', 'Sam', 'Kole', 'Frank', 'Cameron']
        expected_sdr_first_names = ['Tyler', 'Jason', 'Alexa', 'Dean']

        def support_request_inbound():

            support_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_hour_ago,
                                                                                    end_date=self.today,
                                                                                    inbound=True, outbound=False,
                                                                                    queue='8814',
                                                                                    cache_timeout=60)
            logging.info("Support Inbound Result: %s", support_response)
            self.assertIsNotNone(support_response)

            for agent in support_response:
                self.assertIn(agent.get('first_name'), expected_support_first_names,
                              'Found unexpected name in Support Inbound Response. Agent Data: %s' % agent)

        def sdr_request_inbound():

            sdr_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_hour_ago,
                                                                                end_date=self.today,
                                                                                inbound=True, outbound=False,
                                                                                queue='8820',
                                                                                cache_timeout=60)
            logging.info("SDR InboundResult: %s", sdr_response)
            self.assertIsNotNone(sdr_response)

            for agent in sdr_response:
                self.assertIn(agent.get('first_name'), expected_sdr_first_names,
                              'Found unexpected name in SDR Inbound Response. Agent Data: %s' % agent)

        def sdr_request_outbound():

            sdr_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_hour_ago,
                                                                                end_date=self.today,
                                                                                inbound=False, outbound=True,
                                                                                queue='8820',
                                                                                cache_timeout=60)
            logging.info("SDR Outbound Result: %s", sdr_response)
            self.assertIsNotNone(sdr_response)

            for agent in sdr_response:
                self.assertIn(agent.get('first_name'), expected_sdr_first_names,
                              'Found unexpected name in SDR Outbound Response. Agent Data: %s' % agent)

        for _ in xrange(1, 20):
            time.sleep(20)
            logging.info("Begin Iteration")
            support_request_inbound()
            time.sleep(1)
            sdr_request_inbound()
            time.sleep(1)
            sdr_request_outbound()
            logging.info("Finish Iteration")
            time.sleep(10)

    def test_expected_response(self):
        expected_support_first_names = ['Andre', 'Jonathon', 'Sam', 'Kole', 'Frank', 'Cameron']
        expected_sdr_first_names = ['Tyler', 'Jason', 'Alexa', 'Dean']

        def support_request_inbound():

            support_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_hour_ago,
                                                                                    end_date=self.today,
                                                                                    inbound=True, outbound=False,
                                                                                    queue='8814')
            logging.info("Support Inbound Result: %s", support_response)
            self.assertIsNotNone(support_response)

            for agent in support_response:
                self.assertIn(agent.get('first_name'), expected_support_first_names,
                              'Found unexpected name in Support Inbound Response. Agent Data: %s' % agent)

        def sdr_request_inbound():

            sdr_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_hour_ago,
                                                                                end_date=self.today,
                                                                                inbound=True, outbound=False,
                                                                                queue='8820')
            logging.info("SDR InboundResult: %s", sdr_response)
            self.assertIsNotNone(sdr_response)

            for agent in sdr_response:
                self.assertIn(agent.get('first_name'), expected_sdr_first_names,
                              'Found unexpected name in SDR Inbound Response. Agent Data: %s' % agent)

        def sdr_request_outbound():

            sdr_response = access_config.office_manager.versature.call_queue_agent_stats(start_date=self.one_hour_ago,
                                                                                end_date=self.today,
                                                                                inbound=False, outbound=True,
                                                                                queue='8820')
            logging.info("SDR Outbound Result: %s", sdr_response)
            self.assertIsNotNone(sdr_response)

            for agent in sdr_response:
                self.assertIn(agent.get('first_name'), expected_sdr_first_names,
                              'Found unexpected name in SDR Outbound Response. Agent Data: %s' % agent)

        for _ in xrange(1, 60):
            time.sleep(60)
            logging.info("Begin Iteration")
            support_request_inbound()
            time.sleep(1)
            sdr_request_inbound()
            time.sleep(1)
            sdr_request_outbound()
            logging.info("Finish Iteration")
