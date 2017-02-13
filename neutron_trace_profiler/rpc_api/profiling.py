# Copyright (c) 2017 Red Hat, Inc
# All Rights Reserved.
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

from oslo_log import helpers as log_helpers
import oslo_messaging

from neutron.common import constants
from neutron.common import rpc as n_rpc


NEUTRON_PROFILER='neutron_profiler'
PROFILER_NAMESPACE='profiler_namespace'

class ProfilingBroadcastRpcApi(object):
    """Publisher-side RPC (stub) for plugin-to-* fanout interaction.
    This class implements the client side of an rpc interface.  The receiver
    side can be found below: ProfilingBroadcastServerRpcCallback.
    """

    def __init__(self):
        target = oslo_messaging.Target(
            topic=NEUTRON_PROFILER, version='1.0',
            namespace=PROFILER_NAMESPACE)
        self.client = n_rpc.get_client(target)

    @log_helpers.log_method_call
    def start_profiling(self, context, id, kwargs):
        """Fan out all the agent resource versions to other servers."""
        cctxt = self.client.prepare(fanout=True)
        cctxt.cast(context, 'start_profiling', id=id, kwargs=kwargs)

    @log_helpers.log_method_call
    def stop_profiling(self, context, id, kwargs):
        """Fan out all the agent resource versions to other servers."""
        cctxt = self.client.prepare(fanout=True)
        cctxt.cast(context, 'stop_profiling', id=id, kwargs=kwargs)


class ProfilingBroadcastServerRpcCallback(object):
    """Receiver-side RPC (implementation) for plugin-to-* interaction.
    This class implements the receiver side of an rpc interface.
    """

    # History
    #   1.0 Initial version

    target = oslo_messaging.Target(
        version='1.0', namespace=PROFILER_NAMESPACE)

    @log_helpers.log_method_call
    def start_profiling(self, context, id, kwargs):
        pass

    @log_helpers.log_method_call
    def stop_profiling(self, context, id, kwargs):
        pass
