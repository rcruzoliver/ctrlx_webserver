"""
    This module provides helper classes to deal with metadata flatbuffers.
"""
from enum import IntEnum

import flatbuffers
from comm.datalayer import (AllowedOperations, DisplayFormat, Extension, Metadata, NodeClass, Reference, LocaleText)

from ctrlxdatalayer.variant import Variant


class ReferenceType:
    """ List of reference types as strings. """

    @classmethod
    def read(cls):
        """ Type when reading a value (absolute node address). """
        return "readType"

    @classmethod
    def read_in(cls):
        """ Input type when reading a value. """
        return "readInType"

    @classmethod
    def read_out(cls):
        """ Output type when reading a value. """
        return "readOutType"

    @classmethod
    def write(cls):
        """ Type when writing a value (absolute node address). Input/Output type are the same. """
        return "writeType"

    @classmethod
    def write_in(cls):
        """ Input type when writing a value. """
        return "writeInType"

    @classmethod
    def write_out(cls):
        """ Output type when writing a value. """
        return "writeOutType"

    @classmethod
    def create(cls):
        """ Type when creating a value (absolute node address). """
        return "createType"

    @classmethod
    def uses(cls):
        """ Referenced (list of) absolute node addresses. """
        return "uses"

    @classmethod
    def has_save(cls):
        """
        Reference to a save node address which needs to be called after
        node change to persist the new value (must be <technology>/admin/cfg/save).
        """
        return "hasSave"


class AllowedOperation(IntEnum):
    """
    Allowed Operation Flags
    """
    NONE = 0x00000
    READ = 0x00001
    WRITE = 0x00010
    CREATE = 0x00100
    DELETE = 0x01000
    BROWSE = 0x10000
    ALL = READ | WRITE | CREATE | DELETE | BROWSE


class MetadataBuilder:
    """ Builds a flatbuffer provided with the metadata information for a Data Layer node. """

    @staticmethod
    def create_metadata(name: str, description: str, unit: str, description_url: str, node_class: NodeClass,
                        read_allowed: bool, write_allowed: bool, create_allowed: bool, delete_allowed: bool,
                        browse_allowed: bool, type_path: str, references: dict = None) -> Variant:
        """
        Creates a metadata Variant object from the given arguments.
        `type_path` is used in conjunction with the allowed operations of the object.
        `references` allow the user to set own references in the metadata object. Set `type_path` to ""
        for full control over references.
        
        Returns:
            Variant: Metadata
        """
        if references is None:
            references = {}
        builder = MetadataBuilder(allowed=AllowedOperation.NONE, description=description,
                                  description_url=description_url)
        allowed = AllowedOperation.NONE
        if read_allowed:
            allowed = allowed | AllowedOperation.READ
            if len(type_path) != 0:
                builder.add_reference(ReferenceType.read(), type_path)
        if write_allowed:
            allowed = allowed | AllowedOperation.WRITE
            if len(type_path) != 0:
                builder.add_reference(ReferenceType.write(), type_path)
        if create_allowed:
            allowed = allowed | AllowedOperation.CREATE
            if len(type_path) != 0:
                builder.add_reference(ReferenceType.create(), type_path)
        if delete_allowed:
            allowed = allowed | AllowedOperation.DELETE
        if browse_allowed:
            allowed = allowed | AllowedOperation.BROWSE

        builder.set_operations(allowed)
        builder.set_display_name(name)
        builder.set_node_class(node_class)
        builder.set_unit(unit)
        
        # Add the custom references
        for key, val in references.items():
            builder.add_reference(key, val)

        return builder.build()

    def __init__(self, allowed: AllowedOperation = AllowedOperation.BROWSE, description: str = "",
                 description_url: str = ""):
        """
        generate MetadataBuilder
        """
        self.__name = ""
        self.__description = description
        self.__description_url = description_url
        self.__unit = ""
        self.__node_class = NodeClass.NodeClass.Node
        self.__allowed = AllowedOperation.ALL
        self.__displayformat = DisplayFormat.DisplayFormat.Auto
        self.set_operations(allowed)
        self.__references = dict([])
        self.__extensions = dict([])
        self.__descriptions = dict([])
        self.__displaynames = dict([])

    def build(self) -> Variant:
        """Build Metadata as Variant

        Returns:
            Variant: Metadata
        """
        # print(version("flatbuffers"))
        return self.__buildV2()

    def __buildV2(self) -> Variant:
        """
        build function flatbuffers 2.x
        """
        builder = flatbuffers.Builder(1024)

        # Serialize AllowedOperations data
        operations = self.__build_operations()

        references = self.__build_references()

        extensions = self.__build_extensions()

        descriptions = self.__build_descriptions()

        displaynames = self.__build_display_names()

        meta = Metadata.MetadataT()
        meta.description = self.__description
        meta.descriptionUrl = self.__description_url
        meta.displayName = self.__name
        meta.unit = self.__unit
        meta.displayFormat = self.__displayformat

        meta.nodeClass = self.__node_class
        meta.operations = operations
        meta.references = references
        meta.extensions = extensions
        meta.descriptions = descriptions
        meta.displayNames = displaynames
        # Prepare strings

        metadata_internal = meta.Pack(builder)

        # Closing operation
        builder.Finish(metadata_internal)

        metadata = Variant()
        metadata.set_flatbuffers(builder.Output())
        return metadata

    def set_unit(self, unit: str):
        """
        set the unit
        """
        self.__unit = unit
        return self

    def set_display_name(self, name: str):
        """
        set the display name
        """
        self.__name = name
        return self

    def set_node_class(self, node_class: NodeClass):
        """
        set the node class
        """
        self.__node_class = node_class
        return self

    def set_operations(self, allowed: AllowedOperation = AllowedOperation.NONE):
        """
        set allowed operations
        """
        self.__allowed = allowed
        return self

    def set_display_format(self, f: DisplayFormat.DisplayFormat.Auto):
        """
        set display format
        """
        self.__displayformat = f
        return self

    def add_reference(self, t: ReferenceType, addr: str):
        """
        add reference
        """
        self.__references[t] = addr

    def add_extensions(self, key: str, val: str):
        """
        add extension
        """
        self.__extensions[key] = val

    def add_localization_description(self, ident: str, txt: str):
        """
        add localization of descriptions
        """
        self.__descriptions[ident] = txt

    def add_localization_display_name(self, ident: str, txt: str):
        """
        add localization of display names
        """
        self.__displaynames[ident] = txt

    def __is_allowed(self, allowed: AllowedOperation) -> bool:
        return (self.__allowed & allowed) == allowed

    def __build_operations(self):
        op = AllowedOperations.AllowedOperationsT()
        op.read = self.__is_allowed(AllowedOperation.READ)
        op.write = self.__is_allowed(AllowedOperation.WRITE)
        op.create = self.__is_allowed(AllowedOperation.CREATE)
        op.delete = self.__is_allowed(AllowedOperation.DELETE)
        op.browse = self.__is_allowed(AllowedOperation.BROWSE)
        return op

    def __add_reference(self, t: ReferenceType, addr: str):
        ref = Reference.ReferenceT()
        ref.type = t
        ref.targetAddress = addr
        return ref

    def __build_references(self):
        refs = []
        for key in sorted(self.__references):
            addr = self.__references[key]
            ref = self.__add_reference(key, addr)
            refs.append(ref)
        return refs

    def __add_extension(self, key: str, val: str):
        ex = Extension.ExtensionT()
        ex.key = key
        ex.value = val
        return ex

    def __build_extensions(self):
        exts = []
        for key in sorted(self.__extensions):
            val = self.__extensions[key]
            ex = self.__add_extension(key, val)
            exts.append(ex)
        return exts

    def __add_local_text(self, ident: str, txt: str):
        lt = LocaleText.LocaleTextT()
        lt.id = ident
        lt.text = txt
        return lt

    def __build_local_texts(self, lst):
        descs = []
        for i in sorted(lst):
            text = lst[i]
            ex = self.__add_local_text(i, text)
            descs.append(ex)
        return descs

    def __build_descriptions(self):
        return self.__build_local_texts(self.__descriptions)

    def __build_display_names(self):
        return self.__build_local_texts(self.__displaynames)