import abc
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Final, Any

from grpclib.client import Channel
from grpclib.server import Stream
from viam.resource.registry import ResourceRPCServiceBase
from viam.resource.types import RESOURCE_TYPE_SERVICE, Subtype
from viam.services.service_base import ServiceBase
from viam.logging import getLogger
from viam.utils import datetime_to_timestamp

from .grpc.matter_grpc import MatterControllerServiceBase, MatterControllerServiceStub
from .grpc.matter_pb2 import CommissionRequest, CommissionResponse

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


class MatterController(ServiceBase):
    SUBTYPE: Final = Subtype("viam-labs", RESOURCE_TYPE_SERVICE, "matter")

    @abc.abstractmethod
    async def commission(self, code: str) -> MatterNodeData:
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
            attributes=json.dumps(response.attributes),
            last_subscription_attempt=response.last_subscription_attempt,
        )
        await stream.send_message(message)


class MatterControllerClient(MatterController):
    def __init__(self, name: str, channel: Channel) -> None:
        self.channel = channel
        self.client = MatterControllerServiceStub(channel)
        super().__init__(name)

    async def commission(self, code: str) -> MatterNodeData:
        request = CommissionRequest(code=code)
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