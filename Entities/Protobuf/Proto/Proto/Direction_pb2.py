# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Proto/Direction.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Proto/Direction.proto',
  package='Entities.Protobuf.Proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x15Proto/Direction.proto\x12\x17\x45ntities.Protobuf.Proto*\x1e\n\tDirection\x12\x07\n\x03\x42UY\x10\x00\x12\x08\n\x04SELL\x10\x01\x62\x06proto3')
)

_DIRECTION = _descriptor.EnumDescriptor(
  name='Direction',
  full_name='Entities.Protobuf.Proto.Direction',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BUY', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SELL', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=50,
  serialized_end=80,
)
_sym_db.RegisterEnumDescriptor(_DIRECTION)

Direction = enum_type_wrapper.EnumTypeWrapper(_DIRECTION)
BUY = 0
SELL = 1


DESCRIPTOR.enum_types_by_name['Direction'] = _DIRECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
