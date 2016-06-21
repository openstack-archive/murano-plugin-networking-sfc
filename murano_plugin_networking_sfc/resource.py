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

import abc

from neutronclient.common import exceptions as n_err

from murano_plugin_networking_sfc import error


class BaseResourceWrapper(object):

    allowed_actions = ['create', 'list', 'show', 'update', 'delete']
    plural_actions = ['list']

    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractproperty
    def plural_name(self):
        pass

    def __init__(self, client):
        self._client = client

    def _get_neutron_function(self, resource_name, action):
        function_name = '{0}_{1}'.format(action, resource_name)
        return getattr(self._client, function_name)

    def _prepare_request(self, params):
        return {self.name: params}

    def create(self, **kwargs):
        request = self._prepare_request(kwargs)
        response = self._get_neutron_function(self.name, 'create')(request)
        return response[self.name]

    def list(self):
        return self._get_neutron_function(self.plural_name, 'list')()

    def show(self, id_):
        try:
            return self._get_neutron_function(self.name, 'show')(id_)
        except n_err.NotFound as exc:
            raise error.NotFound(exc.message)

    def update(self, id_, **kwargs):
        kwargs['id'] = id_
        request = self._prepare_request(kwargs)
        try:
            response = self._get_neutron_function(self.name, 'update')(request)
        except n_err.NotFound as exc:
            raise error.NotFound(exc.message)
        return response[self.name]

    def delete(self, id_):
        try:
            return self._get_neutron_function(self.name, 'delete')(id_)
        except n_err.NotFound as exc:
            raise error.NotFound(exc.message)


class PortChain(BaseResourceWrapper):

    name = 'port_chain'
    plural_name = '{0}s'.format(name)


class PortPair(BaseResourceWrapper):

    name = 'port_pair'
    plural_name = '{0}s'.format(name)


class PortPairGroup(BaseResourceWrapper):

    name = 'port_pair_group'
    plural_name = '{0}s'.format(name)


class FlowClassifier(BaseResourceWrapper):

    name = 'flow_classifier'
    plural_name = '{0}s'.format(name)
