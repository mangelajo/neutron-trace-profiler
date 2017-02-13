import abc

from neutron_lib.api import extensions as api_extensions

from neutron.api import extensions
from neutron.api.v2 import base
from neutron.api.v2 import resource_helper
from neutron_lib.plugins import directory


RESOURCE_ATTRIBUTE_MAP = {
        'profilingsessions': {
                    'id': {'allow_post': True, 'allow_put': False,
                           'validate': {'type:string': None},
                           'is_visible': True},
                    'flags': {'allow_post': True, 'allow_put': True,
                              'validate': {'type:string': None},
                              'is_visible': True},
                    'path': {'allow_post': False, 'allow_put': False,
                             'validate': {'type:string': None},
                             'is_visible': True}
        }
}


class Profiler_extension(api_extensions.ExtensionDescriptor):

    """API extension for handling the profiler extension."""

    @classmethod
    def get_name(cls):
        return "Profiler extension"

    @classmethod
    def get_alias(cls):
        return "profiler-extension"

    @classmethod
    def get_description(cls):
        return ("Provides REST API extensions to do python profiling across "
                "neutron services")

    @classmethod
    def get_namespace(cls):
        return \
            "http://docs.openstack.org/ext/neutron/profilerextension/api/v1.0"

    @classmethod
    def get_updated(cls):
        return "2017-02-13T04:20:00-00:00"

    @classmethod
    def get_resources(cls):
        """Returns Extended Resources."""
        resources = []
        plugin = directory.get_plugin('TRACE_PROFILER')
        plural_mappings = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP)
        for collection in RESOURCE_ATTRIBUTE_MAP:
            controller = base.create_resource(
                collection, plural_mappings[collection], plugin,
                RESOURCE_ATTRIBUTE_MAP[collection])
            resource = extensions.ResourceExtension(collection, controller)
            resources.append(resource)
        return resources

    def get_extended_resources(self, version):
        if version == "2.0":
            return RESOURCE_ATTRIBUTE_MAP
        else:
            return {}


class ProfilerServicePluginBase(object):

    @abc.abstractmethod
    def get_profilingsessions(self, context, filters=None, fields=None,
                               sorts=None, limit=None, marker=None,
                               page_reverse=False):
        pass

    @abc.abstractmethod
    def get_profilingsession(self, context, id, fields=None):
        pass

    @abc.abstractmethod
    def create_profilingsession(self, context, profilingsession):
        pass

    @abc.abstractmethod
    def delete_profilingsession(self, context, id):
        pass

    @abc.abstractmethod
    def update_profilingsession(self, context, id, profilingsession):
        pass


