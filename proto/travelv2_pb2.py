# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/travelv2.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from proto import param_pb2 as proto_dot_param__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14proto/travelv2.proto\x12!com.mimikko.app.api.play.travelV2\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x11proto/param.proto\"9\n\x17ListTravelRecordRequest\x12\x0c\n\x04page\x18\x01 \x01(\x05\x12\x10\n\x08pageSize\x18\x02 \x01(\x05\"\x8d\x01\n\x18ListTravelRecordResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12\x42\n\x07\x63ontent\x18\x04 \x03(\x0b\x32\x31.com.mimikko.app.api.play.travelV2.GetTravelReply\"\xee\x01\n\x0eGetTravelReply\x12\x10\n\x08recordId\x18\x01 \x01(\x03\x12H\n\x0btravelGroup\x18\x05 \x01(\x0b\x32\x33.com.mimikko.app.api.play.travelV2.TravelGroupReply\x12\x46\n\ntravelArea\x18\x06 \x01(\x0b\x32\x32.com.mimikko.app.api.play.travelV2.TravelAreaReply\x12\x1b\n\x13\x63haracterUpperLimit\x18\n \x01(\x05\x12\x1b\n\x13\x63haracterIdleAmount\x18\x0b \x01(\x05\"\x9b\x05\n\x10TravelGroupReply\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05\x63over\x18\x03 \x01(\t\x12\x11\n\ttraveling\x18\x04 \x01(\x08\x12\x0c\n\x04\x64\x65sc\x18\x05 \x01(\t\x12\x11\n\ttotalTime\x18\x06 \x01(\x05\x12\x0e\n\x06upTime\x18\x07 \x01(\x05\x12+\n\x07\x65ndTime\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bmatchColors\x18\t \x01(\t\x12\x13\n\x0brewardTypes\x18\n \x03(\t\x12\x1c\n\x14possibleRewardAmount\x18\x0b \x01(\x05\x12:\n\x06status\x18\x0c \x01(\x0e\x32*.com.mimikko.app.api.play.param.PlayStatus\x12O\n\x13travelingCharacters\x18\r \x03(\x0b\x32\x32.com.mimikko.app.api.play.param.PlayCharacterReply\x12Q\n\x0etravelConsumes\x18\x0e \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply\x12S\n\x10necessaryRewards\x18\x0f \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply\x12R\n\x0fpossibleRewards\x18\x10 \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply\x12\x1c\n\x14rewardRandomDropDesc\x18\x11 \x01(\t\"\xb7\x02\n\x0fTravelAreaReply\x12\x0e\n\x06\x61reaId\x18\x01 \x01(\x03\x12\x10\n\x08\x61reaName\x18\x02 \x01(\t\x12\x11\n\tareaCover\x18\x03 \x01(\t\x12\x18\n\x10\x61reaTravelAmount\x18\x04 \x01(\x05\x12\x1e\n\x16\x61reaTravelRemainAmount\x18\x05 \x01(\x05\x12\x1b\n\x13\x63haracterIdleAmount\x18\x06 \x01(\x05\x12J\n\x07rewards\x18\x07 \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply\x12L\n\tpostCards\x18\x08 \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply\"7\n\x15ListTravelAreaRequest\x12\x0c\n\x04page\x18\x01 \x01(\x05\x12\x10\n\x08pageSize\x18\x02 \x01(\x05\"\x8c\x01\n\x16ListTravelAreaResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12\x43\n\x07\x63ontent\x18\x04 \x03(\x0b\x32\x32.com.mimikko.app.api.play.travelV2.TravelAreaReply\"H\n\x16ListTravelGroupRequest\x12\x0e\n\x06\x61reaId\x18\x01 \x01(\x03\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\"\x8e\x01\n\x17ListTravelGroupResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12\x44\n\x07\x63ontent\x18\x04 \x03(\x0b\x32\x33.com.mimikko.app.api.play.travelV2.TravelGroupReply\"M\n\rTravelRequest\x12\x0e\n\x06\x61reaId\x18\x01 \x01(\x03\x12\x15\n\rtravelGroupId\x18\x02 \x01(\x03\x12\x15\n\rcharacterCode\x18\x03 \x03(\t\"\x10\n\x0eTravelResponse\"X\n\x1d\x43\x61lculateTravelConsumeRequest\x12\x0e\n\x06\x61reaId\x18\x01 \x01(\x03\x12\x0f\n\x07groupId\x18\x02 \x01(\x03\x12\x16\n\x0e\x63haracterCodes\x18\x03 \x03(\t\"s\n\x1e\x43\x61lculateTravelConsumeResponse\x12Q\n\x0etravelConsumes\x18\x01 \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply\"N\n\x1bListTravelsCharacterRequest\x12\x0f\n\x07groupId\x18\x01 \x01(\x03\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\"\x92\x01\n\x1cListTravelsCharacterResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12\x43\n\x07\x63ontent\x18\x04 \x03(\x0b\x32\x32.com.mimikko.app.api.play.param.PlayCharacterReply\"8\n\x15GetTravelGroupRequest\x12\x0e\n\x06\x61reaId\x18\x01 \x01(\x03\x12\x0f\n\x07groupId\x18\x02 \x01(\x03\"\xf6\x01\n\x16GetTravelGroupResponse\x12\x10\n\x08recordId\x18\x01 \x01(\x03\x12H\n\x0btravelGroup\x18\x05 \x01(\x0b\x32\x33.com.mimikko.app.api.play.travelV2.TravelGroupReply\x12\x46\n\ntravelArea\x18\x06 \x01(\x0b\x32\x32.com.mimikko.app.api.play.travelV2.TravelAreaReply\x12\x1b\n\x13\x63haracterUpperLimit\x18\n \x01(\x05\x12\x1b\n\x13\x63haracterIdleAmount\x18\x0b \x01(\x05\"$\n\x16GetTravelRecordRequest\x12\n\n\x02id\x18\x01 \x01(\x03\"\xf7\x01\n\x17GetTravelRecordResponse\x12\x10\n\x08recordId\x18\x01 \x01(\x03\x12H\n\x0btravelGroup\x18\x05 \x01(\x0b\x32\x33.com.mimikko.app.api.play.travelV2.TravelGroupReply\x12\x46\n\ntravelArea\x18\x06 \x01(\x0b\x32\x32.com.mimikko.app.api.play.travelV2.TravelAreaReply\x12\x1b\n\x13\x63haracterUpperLimit\x18\n \x01(\x05\x12\x1b\n\x13\x63haracterIdleAmount\x18\x0b \x01(\x05\"(\n\x1aReceiveTravelRewardRequest\x12\n\n\x02id\x18\x01 \x01(\x03\"\xb7\x01\n\x1bReceiveTravelRewardResponse\x12J\n\x07rewards\x18\x01 \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply\x12L\n\tpostCards\x18\x02 \x03(\x0b\x32\x39.com.mimikko.app.api.play.param.MaterialScalarDetailReply2\x90\n\n\x08TravelV2\x12\x8d\x01\n\x10ListTravelRecord\x12:.com.mimikko.app.api.play.travelV2.ListTravelRecordRequest\x1a;.com.mimikko.app.api.play.travelV2.ListTravelRecordResponse\"\x00\x12\x87\x01\n\x0eListTravelArea\x12\x38.com.mimikko.app.api.play.travelV2.ListTravelAreaRequest\x1a\x39.com.mimikko.app.api.play.travelV2.ListTravelAreaResponse\"\x00\x12\x8a\x01\n\x0fListTravelGroup\x12\x39.com.mimikko.app.api.play.travelV2.ListTravelGroupRequest\x1a:.com.mimikko.app.api.play.travelV2.ListTravelGroupResponse\"\x00\x12o\n\x06Travel\x12\x30.com.mimikko.app.api.play.travelV2.TravelRequest\x1a\x31.com.mimikko.app.api.play.travelV2.TravelResponse\"\x00\x12\x9f\x01\n\x16\x43\x61lculateTravelConsume\x12@.com.mimikko.app.api.play.travelV2.CalculateTravelConsumeRequest\x1a\x41.com.mimikko.app.api.play.travelV2.CalculateTravelConsumeResponse\"\x00\x12\x99\x01\n\x14ListTravelsCharacter\x12>.com.mimikko.app.api.play.travelV2.ListTravelsCharacterRequest\x1a?.com.mimikko.app.api.play.travelV2.ListTravelsCharacterResponse\"\x00\x12\x87\x01\n\x0eGetTravelGroup\x12\x38.com.mimikko.app.api.play.travelV2.GetTravelGroupRequest\x1a\x39.com.mimikko.app.api.play.travelV2.GetTravelGroupResponse\"\x00\x12\x8a\x01\n\x0fGetTravelRecord\x12\x39.com.mimikko.app.api.play.travelV2.GetTravelRecordRequest\x1a:.com.mimikko.app.api.play.travelV2.GetTravelRecordResponse\"\x00\x12\x96\x01\n\x13ReceiveTravelReward\x12=.com.mimikko.app.api.play.travelV2.ReceiveTravelRewardRequest\x1a>.com.mimikko.app.api.play.travelV2.ReceiveTravelRewardResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.travelv2_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LISTTRAVELRECORDREQUEST._serialized_start=111
  _LISTTRAVELRECORDREQUEST._serialized_end=168
  _LISTTRAVELRECORDRESPONSE._serialized_start=171
  _LISTTRAVELRECORDRESPONSE._serialized_end=312
  _GETTRAVELREPLY._serialized_start=315
  _GETTRAVELREPLY._serialized_end=553
  _TRAVELGROUPREPLY._serialized_start=556
  _TRAVELGROUPREPLY._serialized_end=1223
  _TRAVELAREAREPLY._serialized_start=1226
  _TRAVELAREAREPLY._serialized_end=1537
  _LISTTRAVELAREAREQUEST._serialized_start=1539
  _LISTTRAVELAREAREQUEST._serialized_end=1594
  _LISTTRAVELAREARESPONSE._serialized_start=1597
  _LISTTRAVELAREARESPONSE._serialized_end=1737
  _LISTTRAVELGROUPREQUEST._serialized_start=1739
  _LISTTRAVELGROUPREQUEST._serialized_end=1811
  _LISTTRAVELGROUPRESPONSE._serialized_start=1814
  _LISTTRAVELGROUPRESPONSE._serialized_end=1956
  _TRAVELREQUEST._serialized_start=1958
  _TRAVELREQUEST._serialized_end=2035
  _TRAVELRESPONSE._serialized_start=2037
  _TRAVELRESPONSE._serialized_end=2053
  _CALCULATETRAVELCONSUMEREQUEST._serialized_start=2055
  _CALCULATETRAVELCONSUMEREQUEST._serialized_end=2143
  _CALCULATETRAVELCONSUMERESPONSE._serialized_start=2145
  _CALCULATETRAVELCONSUMERESPONSE._serialized_end=2260
  _LISTTRAVELSCHARACTERREQUEST._serialized_start=2262
  _LISTTRAVELSCHARACTERREQUEST._serialized_end=2340
  _LISTTRAVELSCHARACTERRESPONSE._serialized_start=2343
  _LISTTRAVELSCHARACTERRESPONSE._serialized_end=2489
  _GETTRAVELGROUPREQUEST._serialized_start=2491
  _GETTRAVELGROUPREQUEST._serialized_end=2547
  _GETTRAVELGROUPRESPONSE._serialized_start=2550
  _GETTRAVELGROUPRESPONSE._serialized_end=2796
  _GETTRAVELRECORDREQUEST._serialized_start=2798
  _GETTRAVELRECORDREQUEST._serialized_end=2834
  _GETTRAVELRECORDRESPONSE._serialized_start=2837
  _GETTRAVELRECORDRESPONSE._serialized_end=3084
  _RECEIVETRAVELREWARDREQUEST._serialized_start=3086
  _RECEIVETRAVELREWARDREQUEST._serialized_end=3126
  _RECEIVETRAVELREWARDRESPONSE._serialized_start=3129
  _RECEIVETRAVELREWARDRESPONSE._serialized_end=3312
  _TRAVELV2._serialized_start=3315
  _TRAVELV2._serialized_end=4611
# @@protoc_insertion_point(module_scope)
