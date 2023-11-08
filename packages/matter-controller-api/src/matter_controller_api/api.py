import abc
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Final, Any, List, cast

from grpclib.client import Channel
from grpclib.server import Stream
from viam.resource.rpc_service_base import ResourceRPCServiceBase
from viam.resource.types import RESOURCE_TYPE_SERVICE, Subtype
from viam.services.service_base import ServiceBase
from viam.logging import getLogger
from viam.utils import datetime_to_timestamp

from .grpc.matter_grpc import MatterControllerServiceBase, MatterControllerServiceStub
from .grpc.matter_pb2 import CommissionRequest, CommissionResponse, DiscoverRequest, DiscoverResponse

LOGGER = getLogger(__name__)


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


@dataclass
class CommissionableNode:
    instanceName: str = None
    hostName: str = None
    port: int = None
    longDiscriminator: int = None
    vendorId: int = None
    productId: int = None
    commissioningMode: int = None
    deviceType: int = None
    deviceName: str = None
    pairingInstruction: str = None
    pairingHint: int = None
    mrpRetryIntervalIdle: int = None
    mrpRetryIntervalActive: int = None
    mrpRetryActiveThreshold: int = None
    supportsTcp: bool = None
    isICDOperatingAsLIT: bool = None
    addresses: List[str] = None
    rotatingId: Optional[str] = None


class MatterController(ServiceBase):
    SUBTYPE: Final = Subtype("viam-labs", RESOURCE_TYPE_SERVICE, "matter")

    @abc.abstractmethod
    async def commission(self, code: str) -> MatterNodeData:
        ...

    @abc.abstractmethod
    async def discover(self) -> List[CommissionableNode]:
        ...


class MatterControllerRPCService(MatterControllerServiceBase, ResourceRPCServiceBase):
    RESOURCE_TYPE = MatterController

    async def Commission(self, stream: Stream[CommissionRequest, CommissionResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        response = await service.commission(request.code)
        LOGGER.info(response)
        message = CommissionResponse(
            node_id=response.node_id,
            date_commissioned=datetime_to_timestamp(response.date_commissioned),
            last_interview=datetime_to_timestamp(response.last_interview),
            interview_version=response.interview_version,
            available=response.available,
            is_bridge=response.is_bridge,
            attributes="{}",
            last_subscription_attempt=response.last_subscription_attempt,
        )
        await stream.send_message(message)

    async def Discover(self, stream: Stream[DiscoverRequest, DiscoverResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        response = await service.discover()
        LOGGER.info(response)
        message = DiscoverResponse(nodes=response if response is not None else [])
        await stream.send_message(message)


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
        )

    async def discover(self) -> List[CommissionableNode]:
        request = DiscoverRequest(name=self.name)
        response: DiscoverResponse = await self.client.Discover(request)
        return cast(list, response.nodes)
