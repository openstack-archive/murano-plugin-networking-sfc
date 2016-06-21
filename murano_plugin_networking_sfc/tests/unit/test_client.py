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

from murano_plugin_networking_sfc import client


class TestNetworkingSFCClient(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch.object(client.NetworkingSFCClient, 'client')
        self.addCleanup(patcher.stop)
        self.n_client = patcher.start()

        self.client = client.NetworkingSFCClient(mock.MagicMock())

    def test_client_function_call(self):
        flow_id = 'flow-id'
        port_pair_group_id = 'port-pair-group-id'
        self.client.createPortChain(flowClassifiers=[flow_id],
                                    portPairGroups=[port_pair_group_id])
        self.n_client.create_port_chain.assert_called_once_with({
            'port_chain': {
                'flow_classifiers': [
                    flow_id,
                ],
                'port_pair_groups': [
                    port_pair_group_id
                ]
            }
        })
