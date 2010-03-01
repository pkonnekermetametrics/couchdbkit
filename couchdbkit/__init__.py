# -*- coding: utf-8 -
#
# This file is part of couchdbkit released under the MIT license. 
# See the NOTICE for more information.

from types import ModuleType
import sys


all_by_module = {
    'couchdbkit.resource':      ['ResourceNotFound', 'ResourceConflict', 
                                'RequestFailed', 'PreconditionFailed', 
                                'CouchdbResource'],
    'couchdbkit.exceptions':    ['InvalidAttachment', 'DuplicatePropertyError',
                                'BadValueError', 'MultipleResultsFound',
                                'NoResultFound', 'ReservedWordError', 
                                'DocsPathNotFound', 'BulkSaveError'],
    'couchdbkit.client':        ['Server', 'Database', 'ViewResults',
                                'View', 'TempView'],
    'couchdbkit.consumer':      ['Consumer'],
    'couchdbkit.external':      ['External'],
    'couchdbkit.loaders':       ['BaseDocsLoader', 'FileSystemDocsLoader'],
    'couchdbkit.schema':        ['Property', 'StringProperty', 'IntegerProperty', 
                                'DecimalProperty', 'BooleanProperty', 'FloatProperty', 
                                'DateTimeProperty', 'DateProperty', 'TimeProperty', 
                                'dict_to_json', 'list_to_json', 'value_to_json', 
                                'value_to_python', 'dict_to_python', 'list_to_python', 
                                'convert_property', 'DocumentSchema', 'DocumentBase', 
                                'QueryMixin', 'AttachmentMixin', 'Document', 'StaticDocument',
                                'SchemaProperty', 'SchemaListProperty', 'ListProperty', 
                                'DictProperty', 'StringListProperty', 'contain']
                            
}

attribute_modules = dict.fromkeys(['exceptions', 'resource', 'client', 'schema'])

object_origins = {}
for module, items in all_by_module.iteritems():
    for item in items:
        object_origins[item] = module


class module(ModuleType):
    """Automatically import objects from the modules."""

    def __getattr__(self, name):
        if name in object_origins:
            module = __import__(object_origins[name], None, None, [name])
            for extra_name in all_by_module[module.__name__]:
                setattr(self, extra_name, getattr(module, extra_name))
            return getattr(module, name)
        elif name in attribute_modules:
            __import__('couchdbkit.' + name)
        return ModuleType.__getattribute__(self, name)


# keep a reference to this module so that it's not garbage collected
old_module = sys.modules['couchdbkit']


try:
    version = __import__('pkg_resources').get_distribution('couchdbkit').version
except:
    version = '?'


# setup the new module and patch it into the dict of loaded modules
new_module = sys.modules['couchdbkit'] = module('couchdbkit')
new_module.__dict__.update({
    '__file__':         __file__,
    '__path__':         __path__,
    '__doc__':          __doc__,
    '__all__':          tuple(object_origins) + tuple(attribute_modules),
    '__docformat__':    'restructuredtext en',
    '__version__':      version
})
