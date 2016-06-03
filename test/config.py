# -*- coding: utf-8 -*-

from versature.resources import Versature
from secrets import VERSATURE_API_URL, VERSATURE_CLIENT_ID, VERSATURE_VENDOR_ID, OFFICE_MANAGER_USER, \
    OFFICE_MANAGER_DOMAIN, OFFICE_MANAGER_PASSWORD, BASIC_USER_USER, BASIC_USER_DOMAIN, BASIC_USER_PASSWORD, \
    RESELLER_USER, RESELLER_DOMAIN, RESELLER_PASSWORD, CALL_QUEUE_USER


__author__ = 'DavidWard'


class Config(object):

    def __init__(self, api_url, client_id, user, domain, password, client_secret=None, vendor_id=None, call_queue_user=None):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.vendor_id = vendor_id
        self.user = user
        self.domain = domain
        self.password = password
        self.call_queue_user = call_queue_user

    @property
    def username(self):
        return '%s@%s' % (self.user, self.domain) if self.user and self.domain else None

    @property
    def versature(self):
        return Versature(username=self.username, password=self.password, client_id=self.client_id,
                         client_secret=self.client_secret, vendor_id=self.vendor_id, api_url=self.api_url)


office_manager_config = Config(api_url=VERSATURE_API_URL,
                               client_id=VERSATURE_CLIENT_ID,
                               vendor_id=VERSATURE_VENDOR_ID,
                               user=OFFICE_MANAGER_USER,
                               domain=OFFICE_MANAGER_DOMAIN,
                               password=OFFICE_MANAGER_PASSWORD,
                               call_queue_user=CALL_QUEUE_USER)

base_user_config = Config(api_url=VERSATURE_API_URL,
                          client_id=VERSATURE_CLIENT_ID,
                          vendor_id=VERSATURE_VENDOR_ID,
                          user=BASIC_USER_USER,
                          domain=BASIC_USER_DOMAIN,
                          password=BASIC_USER_PASSWORD)

reseller_config = Config(api_url=VERSATURE_API_URL,
                         client_id=VERSATURE_CLIENT_ID,
                         vendor_id=VERSATURE_VENDOR_ID,
                         user=RESELLER_USER,
                         domain=RESELLER_DOMAIN,
                         password=RESELLER_PASSWORD)