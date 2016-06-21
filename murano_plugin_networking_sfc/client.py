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

from murano_plugin_networking_sfc import common
from murano_plugin_networking_sfc import config
from murano_plugin_networking_sfc import resource

CONF = cfg.CONF


class _BaseNeutronClient(object):
    def __init__(self, this):
        self._owner = this.find_owner('io.murano.Environment')

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


class NetworkingSFCClient(_BaseNeutronClient):

    resources = [
        resource.PortChain,
        resource.PortPair,
        resource.PortPairGroup,
        resource.FlowClassifier,
    ]

    def __init__(self, this):
        super(NetworkingSFCClient, self).__init__(this)

        # TODO(asaprykin): Construct in metaclass
        self._methods = {}
        for rs_cls in self.resources:
            resource_obj = rs_cls(self.client)
            for action in resource_obj.allowed_actions:
                if action in resource_obj.plural_actions:
                    name = resource_obj.plural_name
                else:
                    name = resource_obj.name
                name = '{0}_{1}'.format(action, name)
                self._methods[name] = getattr(resource_obj, action)

    def __getattr__(self, name):
        name = common.camel_case_to_underscore(name)
        try:
            return common.convention_wrapper(self._methods[name])
        except KeyError:
            raise AttributeError(
                "'{0}' object has no attribute '{1}'".format(
                    self.__class__.__name__, name))
