"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
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