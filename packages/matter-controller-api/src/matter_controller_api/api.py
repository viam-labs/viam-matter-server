from __future__ import annotations
import abc
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Final, Any, List, cast, Optional, Literal, NewType

from grpclib.client import Channel
from grpclib.server import Stream
from viam.resource.rpc_service_base import ResourceRPCServiceBase
from viam.resource.types import RESOURCE_TYPE_SERVICE, Subtype
from viam.services.service_base import ServiceBase
from viam.logging import getLogger
from viam.utils import datetime_to_timestamp

from .grpc.matter_grpc import MatterControllerServiceBase, MatterControllerServiceStub
from .grpc.matter_pb2 import (
    CommissionRequest,
    CommissionResponse,
    DiscoverRequest,
    DiscoverResponse,
    CommandRequest,
    CommandResponse,
    Command,
)

LOGGER = getLogger(__name__)
CommandString = Literal["LIGHT_TOGGLE", "LIGHT_ON", "LIGHT_OFF"]


@dataclass
class MatterNodeData:
    node_id: int
    date_commissioned: datetime
    last_interview: datetime
    interview_version: int
    available: bool = False
    is_bridge: bool = False
    attributes: dict[str, Any] = field(default_factory=dict)
    last_subscription_attempt: float = 0
    endpoint_ids: List[int]


@dataclass
class CommissionableNode:
    instanceName: str | None = None
    hostName: str | None = None
    port: int | None = None
    longDiscriminator: int | None = None
    vendorId: int | None = None
    productId: int | None = None
    commissioningMode: int | None = None
    deviceType: int | None = None
    deviceName: str | None = None
    pairingInstruction: str | None = None
    pairingHint: int | None = None
    mrpRetryIntervalIdle: int | None = None
    mrpRetryIntervalActive: int | None = None
    mrpRetryActiveThreshold: int | None = None
    supportsTcp: bool | None = None
    isICDOperatingAsLIT: bool | None = None
    addresses: List[str] | None = None
    rotatingId: Optional[str] = None


class MatterController(ServiceBase):
    SUBTYPE: Final = Subtype("viam-labs", RESOURCE_TYPE_SERVICE, "matter")

    @abc.abstractmethod
    async def commission(self, code: str) -> MatterNodeData:
        ...

    @abc.abstractmethod
    async def discover(self) -> List[CommissionableNode]:
        ...

    @abc.abstractmethod
    async def command_device(
        self,
        node_id: int,
        endpoint_id: int,
        command_name: CommandString,
        payload: dict,
    ) -> bool:
        ...


class MatterControllerRPCService(MatterControllerServiceBase, ResourceRPCServiceBase):
    RESOURCE_TYPE = MatterController

    async def Commission(self, stream: Stream[CommissionRequest, CommissionResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        response: dict = await service.commission(request.code)
        LOGGER.info(response)
        message = CommissionResponse(
            node_id=response.get("node_id"),
            date_commissioned=datetime_to_timestamp(response.get("date_commissioned")),
            last_interview=datetime_to_timestamp(response.get("last_interview")),
            interview_version=response.get("interview_version"),
            available=response.get("available"),
            is_bridge=response.get("is_bridge"),
            attributes=response.get("attributes"),
            last_subscription_attempt=response.last_subscription_attempt,
            endpoint_ids=response.get("endpoint_ids"),
        )
        await stream.send_message(message)

    async def Discover(self, stream: Stream[DiscoverRequest, DiscoverResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        response = await service.discover()
        LOGGER.info(response)
        nodes = (
            [
                DiscoverResponse.CommissionableNode(
                    instanceName=node.instanceName,
                    hostName=node.hostName,
                    port=node.port,
                    longDiscriminator=node.longDiscriminator,
                    vendorId=node.vendorId,
                    productId=node.productId,
                    commissioningMode=node.commissioningMode,
                    deviceType=node.deviceType,
                    deviceName=node.deviceName,
                    pairingInstruction=node.pairingInstruction,
                    pairingHint=node.pairingHint,
                    mrpRetryIntervalIdle=node.mrpRetryIntervalIdle,
                    mrpRetryIntervalActive=node.mrpRetryIntervalActive,
                    mrpRetryActiveThreshold=0,
                    supportsTcp=node.supportsTcp,
                    addresses=node.addresses,
                    rotatingId=node.rotatingId,
                )
                for node in response
            ]
            if response is not None
            else []
        )
        message = DiscoverResponse(nodes=nodes)
        await stream.send_message(message)

    async def CommandDevice(self, stream: Stream[CommandRequest, CommandResponse]):
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        response = await service.command_device(
            node_id=request.node_id,
            endpoint_id=request.endpoint_id,
            command_name=Command.Name(request.command_name),
            payload=request.payload,
        )
        await stream.send_message(CommandResponse(success=response))


class MatterControllerClient(MatterController):
    def __init__(self, name: str, channel: Channel) -> None:
        self.channel = channel
        self.client = MatterControllerServiceStub(channel)
        super().__init__(name)

    async def commission(self, code: str) -> MatterNodeData:
        request = CommissionRequest(name=self.name, code=code)
        response: CommissionResponse = await self.client.Commission(request)
        return MatterNodeData(
            node_id=response.node_id,
            date_commissioned=response.date_commissioned.ToDatetime(),
            last_interview=response.last_interview.ToDatetime(),
            interview_version=response.interview_version,
            available=response.available,
            is_bridge=response.is_bridge,
            attributes=json.loads(response.attributes),
            last_subscription_attempt=response.last_subscription_attempt,
            endpoint_ids=response.endpoint_ids,
        )

    async def discover(self) -> List[CommissionableNode]:
        request = DiscoverRequest(name=self.name)
        response: DiscoverResponse = await self.client.Discover(request)
        return cast(list, response.nodes)

    async def command_device(
        self,
        node_id: int,
        endpoint_id: int,
        command_name: CommandString,
        payload: dict,
    ) -> bool:
        request = CommandRequest(
            name=self.name,
            node_id=node_id,
            endpoint_id=endpoint_id,
            command_name=Command.Value(command_name),
            payload=json.dumps(payload),
        )
        response: CommandResponse = await self.client.CommandDevice(request)
        return response.success
