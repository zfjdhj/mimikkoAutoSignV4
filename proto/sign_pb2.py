# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/sign.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10proto/sign.proto\x12 com.mimikko.app.api.general.sign\"\x0f\n\rEMPTY_request\"O\n\x08response\x12\x16\n\x0e\x63ontinuousSign\x18\x01 \x01(\x05\x12\x11\n\ttodaySign\x18\x02 \x01(\x08\x12\x18\n\x10\x63ontinuousReward\x18\x03 \x03(\t\" \n\x07request\x12\x15\n\rcharacterCode\x18\x01 \x01(\t\"\x9b\x01\n\tresponse2\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12\x10\n\x08isReSign\x18\x02 \x01(\x08\x12\r\n\x05\x63over\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\x0e\n\x06source\x18\x05 \x01(\t\x12\x39\n\x06reward\x18\x06 \x03(\x0b\x32).com.mimikko.app.api.general.sign.rewards\"\x8a\x01\n\x07rewards\x12\x1a\n\x12rewardMaterialCode\x18\x01 \x01(\t\x12\x1a\n\x12rewardMaterialName\x18\x02 \x01(\t\x12\x18\n\x10rewardScalarCode\x18\x03 \x01(\t\x12\x18\n\x10rewardScalarName\x18\x04 \x01(\t\x12\x13\n\x0brewardvalue\x18\x05 \x01(\x05\x32\xdc\x01\n\x04Sign\x12r\n\x11GetUserSignStatus\x12/.com.mimikko.app.api.general.sign.EMPTY_request\x1a*.com.mimikko.app.api.general.sign.response\"\x00\x12`\n\x04Sign\x12).com.mimikko.app.api.general.sign.request\x1a+.com.mimikko.app.api.general.sign.response2\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.sign_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY_REQUEST._serialized_start=54
  _EMPTY_REQUEST._serialized_end=69
  _RESPONSE._serialized_start=71
  _RESPONSE._serialized_end=150
  _REQUEST._serialized_start=152
  _REQUEST._serialized_end=184
  _RESPONSE2._serialized_start=187
  _RESPONSE2._serialized_end=342
  _REWARDS._serialized_start=345
  _REWARDS._serialized_end=483
  _SIGN._serialized_start=486
  _SIGN._serialized_end=706
# @@protoc_insertion_point(module_scope)
