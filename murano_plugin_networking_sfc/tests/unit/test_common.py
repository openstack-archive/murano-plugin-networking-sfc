#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest

from murano_plugin_networking_sfc import common


class TestNameConverters(unittest.TestCase):

    names = [
        ('spam', 'spam'),
        ('spam_eggs', 'spamEggs'),
        ('spam_eggs_bacon', 'spamEggsBacon'),
        ('_spam_eggs', '_spamEggs'),
        ('SPAM_EGGS', 'SPAM_EGGS'),
        ('_SPAM_EGGS', '_SPAM_EGGS')
    ]

    def test_unserscore_to_camel_case(self):
        for underscore, camel_case in self.names:
            self.assertEqual(common.underscore_to_camel_case(underscore),
                             camel_case)

    def test_camel_case_to_underscore(self):
        for underscore, camel_case in self.names:
            self.assertEqual(common.camel_case_to_underscore(camel_case),
                             underscore)
