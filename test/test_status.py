import unittest

import lissandra

from .test_util import BaseTest


class TestStatus(BaseTest):
    def test_all_fields_work(self):
        status = lissandra.get_status("EUW")
        self.assertIsNotNone(status.hostname)
        self.assertIsNotNone(status.name)
        self.assertIsNotNone(status.region)
        self.assertIsNotNone(status.slug)
        for service in status.services:
            self.assertIsNotNone(service.slug)
            self.assertIsNotNone(service.name)
            self.assertIsNotNone(service.incidents)
            self.assertIsNotNone(service.status)
            for incident in service.incidents:
                self.assertIsNotNone(incident.active)
                self.assertIsNotNone(incident.created)
                self.assertIsNotNone(incident.id)
                self.assertIsNotNone(incident.updates)
                for update in incident.updates:
                    self.assertIsNotNone(update.created)
                    self.assertIsNotNone(update.author)
                    self.assertIsNotNone(update.content)
                    self.assertIsNotNone(update.severity)
                    self.assertIsNotNone(update.translations)
                    self.assertIsNotNone(update.updated)
                    print(update.__dict__)
                    for translation in update.translations:
                        self.assertIsNotNone(translation.content)
                        self.assertIsNotNone(translation.locale)
                        self.assertIsNotNone(translation.heading)
