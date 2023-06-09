# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/character.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import material_pb2 as proto_dot_material__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15proto/character.proto\x12%com.mimikko.app.api.general.character\x1a\x14proto/material.proto\".\n\x15\x45nergyExchangeRequest\x12\x15\n\rcharacterCode\x18\x01 \x01(\t\"!\n\x08response\x12\x15\n\rcharacterCode\x18\x01 \x01(\t\"X\n\x14ListCharacterRequest\x12\x10\n\x08typeCode\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12\x0e\n\x06orders\x18\x05 \x01(\t\"\x85\x01\n\tresponse2\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12I\n\x07\x63ontent\x18\x04 \x03(\x0b\x32\x38.com.mimikko.app.api.general.character.GetCharacterReply\"\xb8\x03\n\x11GetCharacterReply\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05level\x18\x03 \x01(\t\x12\x12\n\nlevelValue\x18\x04 \x01(\x05\x12\x16\n\x0e\x65xistNextLevel\x18\x05 \x01(\x05\x12\x0e\n\x06\x61vatar\x18\x06 \x01(\t\x12\x17\n\x0fstorietteLatest\x18\x07 \x01(\t\x12\x44\n\nstatistics\x18\x08 \x03(\x0b\x32\x30.com.mimikko.app.api.general.material.Statistics\x12I\n\x08packages\x18\t \x03(\x0b\x32\x37.com.mimikko.app.api.general.character.PackageTypeReply\x12\x45\n\nattributes\x18\n \x03(\x0b\x32\x31.com.mimikko.app.api.general.character.Attributes\x12K\n\x06origin\x18\x0b \x01(\x0b\x32;.com.mimikko.app.api.general.character.OriginCharacterReply\"\xa3\x01\n\x10PackageTypeReply\x12@\n\x04type\x18\x01 \x01(\x0e\x32\x32.com.mimikko.app.api.general.character.PackageType\x12M\n\rmaterialReply\x18\x02 \x01(\x0b\x32\x36.com.mimikko.app.api.general.material.GetMaterialReply\"(\n\nAttributes\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\xf6\x01\n\x14OriginCharacterReply\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05level\x18\x03 \x01(\t\x12\x12\n\nlevelValue\x18\x04 \x01(\x05\x12\x0e\n\x06\x61vatar\x18\x05 \x01(\t\x12H\n\x08packages\x18\x06 \x01(\x0b\x32\x36.com.mimikko.app.api.general.material.GetMaterialReply\x12\x45\n\nattributes\x18\x07 \x01(\x0b\x32\x31.com.mimikko.app.api.general.character.Attributes\"2\n\"CharacterLevelManualUpgradeRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\"\x07\n\x05\x45MPTY\"_\n\x1fListCharacterLevelRewardRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12\x0e\n\x06orders\x18\x05 \x03(\t\"\x8d\x01\n\tresponse4\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08pageSize\x18\x03 \x01(\x05\x12Q\n\x07\x63ontent\x18\x04 \x03(\x0b\x32@.com.mimikko.app.api.general.character.CharacterLevelRewardReply\"\xb6\x02\n\x19\x43haracterLevelRewardReply\x12\x0f\n\x07levelId\x18\x01 \x01(\x03\x12\x1a\n\x12rewardCollectionId\x18\x02 \x01(\x03\x12\x12\n\nlevelValue\x18\x03 \x01(\x05\x12\r\n\x05level\x18\x04 \x01(\t\x12\x15\n\rachievedLevel\x18\x05 \x01(\x08\x12\x10\n\x08progress\x18\x06 \x01(\x02\x12V\n\x06status\x18\x07 \x01(\x0e\x32\x46.com.mimikko.app.api.general.character.CharacterLevelRewardReplyStatus\x12H\n\x07rewards\x18\x08 \x03(\x0b\x32\x37.com.mimikko.app.api.general.character.LevelRewardReply\"X\n\x10LevelRewardReply\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\x05\x12\r\n\x05\x63over\x18\x03 \x01(\t\x12\x0b\n\x03num\x18\x04 \x01(\x05\x12\x0c\n\x04\x64\x65sc\x18\x05 \x01(\t\"Q\n\"ReceiveCharacterLevelRewardRequest\x12\x0f\n\x07levelId\x18\x01 \x01(\x03\x12\x1a\n\x12rewardCollectionId\x18\x02 \x01(\x03*)\n\x0bPackageType\x12\t\n\x05MODEL\x10\x00\x12\x06\n\x02\x41I\x10\x01\x12\x07\n\x03\x45XP\x10\x02*O\n\x1f\x43haracterLevelRewardReplyStatus\x12\x0c\n\x08RECEIVED\x10\x00\x12\r\n\tAVAILABLE\x10\x01\x12\x0f\n\x0bUNCLAIMABLE\x10\x02\x32\xe1\x05\n\tCharacter\x12\x81\x01\n\x0e\x45nergyExchange\x12<.com.mimikko.app.api.general.character.EnergyExchangeRequest\x1a/.com.mimikko.app.api.general.character.response\"\x00\x12\x80\x01\n\rListCharacter\x12;.com.mimikko.app.api.general.character.ListCharacterRequest\x1a\x30.com.mimikko.app.api.general.character.response2\"\x00\x12\x98\x01\n\x1b\x43haracterLevelManualUpgrade\x12I.com.mimikko.app.api.general.character.CharacterLevelManualUpgradeRequest\x1a,.com.mimikko.app.api.general.character.EMPTY\"\x00\x12\x96\x01\n\x18ListCharacterLevelReward\x12\x46.com.mimikko.app.api.general.character.ListCharacterLevelRewardRequest\x1a\x30.com.mimikko.app.api.general.character.response4\"\x00\x12\x98\x01\n\x1bReceiveCharacterLevelReward\x12I.com.mimikko.app.api.general.character.ReceiveCharacterLevelRewardRequest\x1a,.com.mimikko.app.api.general.character.EMPTY\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.character_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PACKAGETYPE._serialized_start=2083
  _PACKAGETYPE._serialized_end=2124
  _CHARACTERLEVELREWARDREPLYSTATUS._serialized_start=2126
  _CHARACTERLEVELREWARDREPLYSTATUS._serialized_end=2205
  _ENERGYEXCHANGEREQUEST._serialized_start=86
  _ENERGYEXCHANGEREQUEST._serialized_end=132
  _RESPONSE._serialized_start=134
  _RESPONSE._serialized_end=167
  _LISTCHARACTERREQUEST._serialized_start=169
  _LISTCHARACTERREQUEST._serialized_end=257
  _RESPONSE2._serialized_start=260
  _RESPONSE2._serialized_end=393
  _GETCHARACTERREPLY._serialized_start=396
  _GETCHARACTERREPLY._serialized_end=836
  _PACKAGETYPEREPLY._serialized_start=839
  _PACKAGETYPEREPLY._serialized_end=1002
  _ATTRIBUTES._serialized_start=1004
  _ATTRIBUTES._serialized_end=1044
  _ORIGINCHARACTERREPLY._serialized_start=1047
  _ORIGINCHARACTERREPLY._serialized_end=1293
  _CHARACTERLEVELMANUALUPGRADEREQUEST._serialized_start=1295
  _CHARACTERLEVELMANUALUPGRADEREQUEST._serialized_end=1345
  _EMPTY._serialized_start=1347
  _EMPTY._serialized_end=1354
  _LISTCHARACTERLEVELREWARDREQUEST._serialized_start=1356
  _LISTCHARACTERLEVELREWARDREQUEST._serialized_end=1451
  _RESPONSE4._serialized_start=1454
  _RESPONSE4._serialized_end=1595
  _CHARACTERLEVELREWARDREPLY._serialized_start=1598
  _CHARACTERLEVELREWARDREPLY._serialized_end=1908
  _LEVELREWARDREPLY._serialized_start=1910
  _LEVELREWARDREPLY._serialized_end=1998
  _RECEIVECHARACTERLEVELREWARDREQUEST._serialized_start=2000
  _RECEIVECHARACTERLEVELREWARDREQUEST._serialized_end=2081
  _CHARACTER._serialized_start=2208
  _CHARACTER._serialized_end=2945
# @@protoc_insertion_point(module_scope)
