# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Status.proto

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
  name='Status.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0cStatus.proto*s\n\x06Status\x12\x0e\n\nSTATUS_NEW\x10\x00\x12\x16\n\x12STATUS_TO_PROVIDER\x10\x01\x12\x11\n\rSTATUS_FILLED\x10\x02\x12\x19\n\x15STATUS_PARTIAL_FILLED\x10\x03\x12\x13\n\x0fSTATUS_REJECTED\x10\x04\x62\x06proto3')
)

_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATUS_NEW', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUS_TO_PROVIDER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUS_FILLED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUS_PARTIAL_FILLED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUS_REJECTED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=16,
  serialized_end=131,
)
_sym_db.RegisterEnumDescriptor(_STATUS)

Status = enum_type_wrapper.EnumTypeWrapper(_STATUS)
STATUS_NEW = 0
STATUS_TO_PROVIDER = 1
STATUS_FILLED = 2
STATUS_PARTIAL_FILLED = 3
STATUS_REJECTED = 4


DESCRIPTOR.enum_types_by_name['Status'] = _STATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)