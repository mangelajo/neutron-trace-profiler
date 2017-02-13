import logging
import server
import threading

from neutron.agent import agent_extension
from neutron.api import extensions
from neutron.callbacks import events
from neutron.callbacks import registry
from neutron.callbacks import resources
from neutron.services import service_base
from neutron_trace_profiler import extensions as ntp_extensions
from oslo_config import cfg


LOG = logging.getLogger(__name__)

PROFILER_PLUGIN_TYPE = 'TRACE_PROFILER'
PROFILER_SOCK_DIR = '/opt/stack/data/neutron/trace_profiler_sock'
PROFILER_TRACE_DIR = '/opt/stack/data/neutron/trace_profiler_files'
TRACE_FORMAT = 'pstat'

ProfilerOpts = [
    cfg.StrOpt(
        'sock_path',
        default=PROFILER_SOCK_DIR,
        help=_("Profiler socket path")),
    cfg.BoolOpt(
        'enabled',
        default=False,
        help=_("Enable Trace Profiler")),
    cfg.StrOpt(
        'trace_format',
        default=TRACE_FORMAT,
        help=_("Profiler trace format")),
    cfg.StrOpt(
        'trace_path',
        default=PROFILER_TRACE_DIR,
        help=_("Profiler trace files path")),
]
cfg.CONF.register_opts(ProfilerOpts, 'trace_profiler')


class Profiler(service_base.ServicePluginBase):

    supported_extension_aliases = ['profiler-extension']

    def __init__(self):
        extensions.append_api_extensions_path(ntp_extensions.__path__)
        super(Profiler, self).__init__()
        if cfg.CONF.trace_profiler.enabled:
            self.subscribe()

        self._sessions = {}

    @classmethod
    def get_plugin_type(cls):
        return PROFILER_PLUGIN_TYPE

    def get_plugin_description(self):
        return "Neutron trace profiler plugin"

    def subscribe(self):
        registry.subscribe(
            process_spawned, resources.PROCESS, events.AFTER_INIT)

    def get_profilingsessions(self, context, filters=None, fields=None,
                               sorts=None, limit=None, marker=None,
                               page_reverse=False):
        #FIXME: this doesn't work as-is because, every service process
        #       has it's own memory map and sessions... :)
        return [session for session in self._sessions.values()]

    def get_profilingsession(self, context, id, fields=None):
        pass

    def create_profilingsession(self, context, profilingsession):
        profiling_session = profilingsession['profilingsession']
        id = profiling_session['id']
        profiling_session['path'] = (
            cfg.CONF.trace_profiler.trace_path + '/' +
            id)
        if id in self._sessions:
            raise "duplicated"
        else:
            # make sure there's no other session running already
            self._sessions[id] = profiling_session

        return profiling_session

    def delete_profilingsession(self, context, id):

        pass

    def update_profilingsession(self, context, id, profilingsession):
        pass



def process_spawned(resource, event, trigger, **kwargs):
    thread = threading.Thread(target=server.start_profiler_server)
    thread.start()


class ProfilerAgentExtension(agent_extension.AgentExtension):
    def initialize(self, connection, driver_type):
        thread = threading.Thread(target=server.start_profiler_server)
        thread.start()

    def consume_api(self, agent_api):
        pass
