"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class CommissionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    CODE_FIELD_NUMBER: builtins.int
    name: builtins.str
    code: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        code: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code", "name", b"name"]) -> None: ...

global___CommissionRequest = CommissionRequest

@typing_extensions.final
class CommissionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NODE_ID_FIELD_NUMBER: builtins.int
    DATE_COMMISSIONED_FIELD_NUMBER: builtins.int
    LAST_INTERVIEW_FIELD_NUMBER: builtins.int
    INTERVIEW_VERSION_FIELD_NUMBER: builtins.int
    AVAILABLE_FIELD_NUMBER: builtins.int
    IS_BRIDGE_FIELD_NUMBER: builtins.int
    ATTRIBUTES_FIELD_NUMBER: builtins.int
    LAST_SUBSCRIPTION_ATTEMPT_FIELD_NUMBER: builtins.int
    node_id: builtins.int
    @property
    def date_commissioned(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def last_interview(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    interview_version: builtins.int
    available: builtins.bool
    is_bridge: builtins.bool
    attributes: builtins.str
    last_subscription_attempt: builtins.float
    def __init__(
        self,
        *,
        node_id: builtins.int = ...,
        date_commissioned: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        last_interview: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        interview_version: builtins.int = ...,
        available: builtins.bool = ...,
        is_bridge: builtins.bool = ...,
        attributes: builtins.str = ...,
        last_subscription_attempt: builtins.float = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["date_commissioned", b"date_commissioned", "last_interview", b"last_interview"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["attributes", b"attributes", "available", b"available", "date_commissioned", b"date_commissioned", "interview_version", b"interview_version", "is_bridge", b"is_bridge", "last_interview", b"last_interview", "last_subscription_attempt", b"last_subscription_attempt", "node_id", b"node_id"]) -> None: ...

global___CommissionResponse = CommissionResponse

@typing_extensions.final
class DiscoverRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name"]) -> None: ...

global___DiscoverRequest = DiscoverRequest

@typing_extensions.final
class DiscoverResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class CommissionableNode(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        INSTANCENAME_FIELD_NUMBER: builtins.int
        HOSTNAME_FIELD_NUMBER: builtins.int
        PORT_FIELD_NUMBER: builtins.int
        LONGDISCRIMINATOR_FIELD_NUMBER: builtins.int
        VENDORID_FIELD_NUMBER: builtins.int
        PRODUCTID_FIELD_NUMBER: builtins.int
        COMMISSIONINGMODE_FIELD_NUMBER: builtins.int
        DEVICETYPE_FIELD_NUMBER: builtins.int
        DEVICENAME_FIELD_NUMBER: builtins.int
        PAIRINGINSTRUCTION_FIELD_NUMBER: builtins.int
        PAIRINGHINT_FIELD_NUMBER: builtins.int
        MRPRETRYINTERVALIDLE_FIELD_NUMBER: builtins.int
        MRPRETRYINTERVALACTIVE_FIELD_NUMBER: builtins.int
        MRPRETRYACTIVETHRESHOLD_FIELD_NUMBER: builtins.int
        SUPPORTSTCP_FIELD_NUMBER: builtins.int
        ISICDOPERATINGASLIT_FIELD_NUMBER: builtins.int
        ADDRESSES_FIELD_NUMBER: builtins.int
        ROTATINGID_FIELD_NUMBER: builtins.int
        instanceName: builtins.str
        hostName: builtins.str
        port: builtins.int
        longDiscriminator: builtins.int
        vendorId: builtins.int
        productId: builtins.int
        commissioningMode: builtins.int
        deviceType: builtins.int
        deviceName: builtins.str
        pairingInstruction: builtins.str
        pairingHint: builtins.int
        mrpRetryIntervalIdle: builtins.int
        mrpRetryIntervalActive: builtins.int
        mrpRetryActiveThreshold: builtins.int
        supportsTcp: builtins.bool
        isICDOperatingAsLIT: builtins.bool
        @property
        def addresses(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
        rotatingId: builtins.str
        def __init__(
            self,
            *,
            instanceName: builtins.str = ...,
            hostName: builtins.str = ...,
            port: builtins.int = ...,
            longDiscriminator: builtins.int = ...,
            vendorId: builtins.int = ...,
            productId: builtins.int = ...,
            commissioningMode: builtins.int = ...,
            deviceType: builtins.int = ...,
            deviceName: builtins.str = ...,
            pairingInstruction: builtins.str = ...,
            pairingHint: builtins.int = ...,
            mrpRetryIntervalIdle: builtins.int = ...,
            mrpRetryIntervalActive: builtins.int = ...,
            mrpRetryActiveThreshold: builtins.int = ...,
            supportsTcp: builtins.bool = ...,
            isICDOperatingAsLIT: builtins.bool = ...,
            addresses: collections.abc.Iterable[builtins.str] | None = ...,
            rotatingId: builtins.str | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["_rotatingId", b"_rotatingId", "rotatingId", b"rotatingId"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["_rotatingId", b"_rotatingId", "addresses", b"addresses", "commissioningMode", b"commissioningMode", "deviceName", b"deviceName", "deviceType", b"deviceType", "hostName", b"hostName", "instanceName", b"instanceName", "isICDOperatingAsLIT", b"isICDOperatingAsLIT", "longDiscriminator", b"longDiscriminator", "mrpRetryActiveThreshold", b"mrpRetryActiveThreshold", "mrpRetryIntervalActive", b"mrpRetryIntervalActive", "mrpRetryIntervalIdle", b"mrpRetryIntervalIdle", "pairingHint", b"pairingHint", "pairingInstruction", b"pairingInstruction", "port", b"port", "productId", b"productId", "rotatingId", b"rotatingId", "supportsTcp", b"supportsTcp", "vendorId", b"vendorId"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal["_rotatingId", b"_rotatingId"]) -> typing_extensions.Literal["rotatingId"] | None: ...

    NODES_FIELD_NUMBER: builtins.int
    @property
    def nodes(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DiscoverResponse.CommissionableNode]: ...
    def __init__(
        self,
        *,
        nodes: collections.abc.Iterable[global___DiscoverResponse.CommissionableNode] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["nodes", b"nodes"]) -> None: ...

global___DiscoverResponse = DiscoverResponse
