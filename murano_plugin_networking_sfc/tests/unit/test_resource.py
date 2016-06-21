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

import mock
import unittest
import uuid

from murano_plugin_networking_sfc import resource


class SampleResource(resource.BaseResourceWrapper):

    name = 'sample'
    plural_name = 'samples'


class TestBaseResourceWrapper(unittest.TestCase):

    def setUp(self):
        self.n_client = mock.MagicMock()

        self.client = SampleResource(self.n_client)

    def test_create_resource(self):
        foo = str(uuid.uuid4())
        bar = 16
        expected_data = {'param_foo': foo, 'param_bar': bar}
        self.n_client.create_sample.side_effect = lambda req: req

        response = self.client.create(param_foo=foo, param_bar=bar)
        self.n_client.create_sample.assert_called_once_with({
            'sample': expected_data,
        })
        self.assertEqual(response, expected_data)

    def test_delete_resource(self):
        self.client.delete(32)
        self.n_client.delete_sample.assert_called_once_with(32)

    def test_list_resources(self):
        self.client.list()
        self.n_client.list_samples.assert_called_once_with()

    def test_show_resource(self):
        self.client.show(64)
        self.n_client.show_sample.assert_called_once_with(64)

    def test_update_resource(self):
        foo = str(uuid.uuid4())
        bar = 16
        expected_data = {'id': 8, 'param_foo': foo, 'param_bar': bar}
        self.n_client.update_sample.side_effect = lambda req: req

        response = self.client.update(8, param_foo=foo, param_bar=bar)
        self.n_client.update_sample.assert_called_once_with({
            'sample': expected_data,
        })
        self.assertEqual(response, expected_data)
