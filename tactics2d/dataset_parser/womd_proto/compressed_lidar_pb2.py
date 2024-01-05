# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: compressed_lidar.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import tactics2d.dataset_parser.womd_proto.dataset_pb2 as dataset__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="compressed_lidar.proto",
    package="waymo.open_dataset",
    syntax="proto2",
    serialized_pb=_b(
        '\n\x16\x63ompressed_lidar.proto\x12\x12waymo.open_dataset\x1a\rdataset.proto"g\n\x14\x43ompressedRangeImage\x12$\n\x1crange_image_delta_compressed\x18\x01 \x01(\x0c\x12)\n!range_image_pose_delta_compressed\x18\x04 \x01(\x0c"2\n\x08Metadata\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x17\n\x0fquant_precision\x18\x02 \x03(\x02"j\n\x10\x44\x65ltaEncodedData\x12\x14\n\x08residual\x18\x01 \x03(\x12\x42\x02\x10\x01\x12\x10\n\x04mask\x18\x02 \x03(\rB\x02\x10\x01\x12.\n\x08metadata\x18\x03 \x01(\x0b\x32\x1c.waymo.open_dataset.Metadata"\xbf\x01\n\x0f\x43ompressedLaser\x12\x30\n\x04name\x18\x01 \x01(\x0e\x32".waymo.open_dataset.LaserName.Name\x12<\n\nri_return1\x18\x02 \x01(\x0b\x32(.waymo.open_dataset.CompressedRangeImage\x12<\n\nri_return2\x18\x03 \x01(\x0b\x32(.waymo.open_dataset.CompressedRangeImage"\xbe\x01\n\x18\x43ompressedFrameLaserData\x12\x33\n\x06lasers\x18\x01 \x03(\x0b\x32#.waymo.open_dataset.CompressedLaser\x12@\n\x12laser_calibrations\x18\x02 \x03(\x0b\x32$.waymo.open_dataset.LaserCalibration\x12+\n\x04pose\x18\x03 \x01(\x0b\x32\x1d.waymo.open_dataset.Transform'
    ),
    dependencies=[dataset__pb2.DESCRIPTOR],
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


_COMPRESSEDRANGEIMAGE = _descriptor.Descriptor(
    name="CompressedRangeImage",
    full_name="waymo.open_dataset.CompressedRangeImage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="range_image_delta_compressed",
            full_name="waymo.open_dataset.CompressedRangeImage.range_image_delta_compressed",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="range_image_pose_delta_compressed",
            full_name="waymo.open_dataset.CompressedRangeImage.range_image_pose_delta_compressed",
            index=1,
            number=4,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=61,
    serialized_end=164,
)


_METADATA = _descriptor.Descriptor(
    name="Metadata",
    full_name="waymo.open_dataset.Metadata",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="shape",
            full_name="waymo.open_dataset.Metadata.shape",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="quant_precision",
            full_name="waymo.open_dataset.Metadata.quant_precision",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=166,
    serialized_end=216,
)


_DELTAENCODEDDATA = _descriptor.Descriptor(
    name="DeltaEncodedData",
    full_name="waymo.open_dataset.DeltaEncodedData",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="residual",
            full_name="waymo.open_dataset.DeltaEncodedData.residual",
            index=0,
            number=1,
            type=18,
            cpp_type=2,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
        ),
        _descriptor.FieldDescriptor(
            name="mask",
            full_name="waymo.open_dataset.DeltaEncodedData.mask",
            index=1,
            number=2,
            type=13,
            cpp_type=3,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b("\020\001")),
        ),
        _descriptor.FieldDescriptor(
            name="metadata",
            full_name="waymo.open_dataset.DeltaEncodedData.metadata",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=218,
    serialized_end=324,
)


_COMPRESSEDLASER = _descriptor.Descriptor(
    name="CompressedLaser",
    full_name="waymo.open_dataset.CompressedLaser",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="waymo.open_dataset.CompressedLaser.name",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="ri_return1",
            full_name="waymo.open_dataset.CompressedLaser.ri_return1",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="ri_return2",
            full_name="waymo.open_dataset.CompressedLaser.ri_return2",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=327,
    serialized_end=518,
)


_COMPRESSEDFRAMELASERDATA = _descriptor.Descriptor(
    name="CompressedFrameLaserData",
    full_name="waymo.open_dataset.CompressedFrameLaserData",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="lasers",
            full_name="waymo.open_dataset.CompressedFrameLaserData.lasers",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="laser_calibrations",
            full_name="waymo.open_dataset.CompressedFrameLaserData.laser_calibrations",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="pose",
            full_name="waymo.open_dataset.CompressedFrameLaserData.pose",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=521,
    serialized_end=711,
)

_DELTAENCODEDDATA.fields_by_name["metadata"].message_type = _METADATA
_COMPRESSEDLASER.fields_by_name["name"].enum_type = dataset__pb2._LASERNAME_NAME
_COMPRESSEDLASER.fields_by_name["ri_return1"].message_type = _COMPRESSEDRANGEIMAGE
_COMPRESSEDLASER.fields_by_name["ri_return2"].message_type = _COMPRESSEDRANGEIMAGE
_COMPRESSEDFRAMELASERDATA.fields_by_name["lasers"].message_type = _COMPRESSEDLASER
_COMPRESSEDFRAMELASERDATA.fields_by_name[
    "laser_calibrations"
].message_type = dataset__pb2._LASERCALIBRATION
_COMPRESSEDFRAMELASERDATA.fields_by_name["pose"].message_type = dataset__pb2._TRANSFORM
DESCRIPTOR.message_types_by_name["CompressedRangeImage"] = _COMPRESSEDRANGEIMAGE
DESCRIPTOR.message_types_by_name["Metadata"] = _METADATA
DESCRIPTOR.message_types_by_name["DeltaEncodedData"] = _DELTAENCODEDDATA
DESCRIPTOR.message_types_by_name["CompressedLaser"] = _COMPRESSEDLASER
DESCRIPTOR.message_types_by_name["CompressedFrameLaserData"] = _COMPRESSEDFRAMELASERDATA

CompressedRangeImage = _reflection.GeneratedProtocolMessageType(
    "CompressedRangeImage",
    (_message.Message,),
    dict(
        DESCRIPTOR=_COMPRESSEDRANGEIMAGE,
        __module__="compressed_lidar_pb2"
        # @@protoc_insertion_point(class_scope:waymo.open_dataset.CompressedRangeImage)
    ),
)
_sym_db.RegisterMessage(CompressedRangeImage)

Metadata = _reflection.GeneratedProtocolMessageType(
    "Metadata",
    (_message.Message,),
    dict(
        DESCRIPTOR=_METADATA,
        __module__="compressed_lidar_pb2"
        # @@protoc_insertion_point(class_scope:waymo.open_dataset.Metadata)
    ),
)
_sym_db.RegisterMessage(Metadata)

DeltaEncodedData = _reflection.GeneratedProtocolMessageType(
    "DeltaEncodedData",
    (_message.Message,),
    dict(
        DESCRIPTOR=_DELTAENCODEDDATA,
        __module__="compressed_lidar_pb2"
        # @@protoc_insertion_point(class_scope:waymo.open_dataset.DeltaEncodedData)
    ),
)
_sym_db.RegisterMessage(DeltaEncodedData)

CompressedLaser = _reflection.GeneratedProtocolMessageType(
    "CompressedLaser",
    (_message.Message,),
    dict(
        DESCRIPTOR=_COMPRESSEDLASER,
        __module__="compressed_lidar_pb2"
        # @@protoc_insertion_point(class_scope:waymo.open_dataset.CompressedLaser)
    ),
)
_sym_db.RegisterMessage(CompressedLaser)

CompressedFrameLaserData = _reflection.GeneratedProtocolMessageType(
    "CompressedFrameLaserData",
    (_message.Message,),
    dict(
        DESCRIPTOR=_COMPRESSEDFRAMELASERDATA,
        __module__="compressed_lidar_pb2"
        # @@protoc_insertion_point(class_scope:waymo.open_dataset.CompressedFrameLaserData)
    ),
)
_sym_db.RegisterMessage(CompressedFrameLaserData)


_DELTAENCODEDDATA.fields_by_name["residual"].has_options = True
_DELTAENCODEDDATA.fields_by_name["residual"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
_DELTAENCODEDDATA.fields_by_name["mask"].has_options = True
_DELTAENCODEDDATA.fields_by_name["mask"]._options = _descriptor._ParseOptions(
    descriptor_pb2.FieldOptions(), _b("\020\001")
)
# @@protoc_insertion_point(module_scope)
