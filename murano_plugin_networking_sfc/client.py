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

from murano.common import auth_utils
from murano.dsl import session_local_storage
from neutronclient.v2_0 import client as n_client
from oslo_config import cfg
import six

from murano_plugin_networking_sfc import config
from murano_plugin_networking_sfc import resource

CONF = cfg.CONF


class _ClientMeta(type):

    def __init__(cls, name, bases, attrs):
        super(_ClientMeta, cls).__init__(name, bases, attrs)

        for resource_obj in attrs['resources']:
            for action in resource_obj.allowed_actions:
                if action in resource_obj.plural_actions:
                    name = resource_obj.plural_name
                else:
                    name = resource_obj.name
                name = '{0}_{1}'.format(action, name)
                setattr(cls, name, getattr(resource_obj, action))


@six.add_metaclass(_ClientMeta)
class _BaseNeutronClient(object):
    def __init__(self, this):
        self._owner = this.find_owner('io.murano.Environment')

    resources = []

    @classmethod
    def init_plugin(cls):
        cls.CONF = config.init_config(CONF)

    @property
    def client(self):
        region = None
        if self._owner is not None:
            region = self._owner['region']
        return self._get_client(region)

    @staticmethod
    @session_local_storage.execution_session_memoize
    def _get_client(region):
        params = auth_utils.get_session_client_parameters(
            service_type='network', conf=CONF, region=region)
        return n_client.Client(**params)


class NetworkingSfcClient(_BaseNeutronClient):

    resources = [
        resource.PortChain,
        resource.PortPair,
        resource.PortPairGroup,
        resource.FlowClassifier,
    ]
