# SPDX-FileCopyrightText: 2023-present HipsterBrown <headhipster@hipsterbrown.com>
#
# SPDX-License-Identifier: Apache-2.0
import asyncio
import os
from typing import ClassVar, Mapping, List
from typing_extensions import Self

from viam.logging import getLogger
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.module.types import Reconfigurable
from viam.resource.registry import Registry, ResourceCreatorRegistration

from matter_controller_api import MatterController, MatterNodeData, CommissionableNode

from matter_server.server.device_controller import MatterDeviceController
from matter_server.server.stack import MatterStack
from matter_server.server.storage import StorageController
from matter_server.server.vendor_info import VendorInfo

LOGGER = getLogger(__name__)
DEFAULT_VENDOR_ID = 0xFFF1
DEFAULT_FABRIC_ID = 1
DEFAULT_PORT = 5580
DEFAULT_STORAGE_PATH = os.path.join("/data")


class MatterControllerServer(MatterController, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("viam-labs", "matter"), "controller")

    started = None

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        matter_server = cls(config.name)
        matter_server.reconfigure(config, dependencies)
        return matter_server

    @classmethod
    def validate(cls, config: ComponentConfig):
        return []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.storage_path = DEFAULT_STORAGE_PATH
        self.vendor_id = DEFAULT_VENDOR_ID
        self.fabric_id = DEFAULT_FABRIC_ID
        self.port = DEFAULT_PORT
        self.logger = LOGGER
        self.loop: asyncio.AbstractEventLoop | None = None
        self.stack = MatterStack(self)
        self.device_controller = MatterDeviceController(self)
        self.storage = StorageController(self)
        self.vendor_info = VendorInfo(self)
        self.command_handlers = {}

        self.started = asyncio.create_task(self.start())
        return

    async def start(self) -> None:
        self.logger.info("Starting the Matter Server")
        self.loop = asyncio.get_running_loop()
        await self.device_controller.initialize()
        await self.storage.start()
        await self.device_controller.start()
        await self.vendor_info.start()
        self.logger.info("Server started!")

    async def commission(self, code: str) -> MatterNodeData:
        data = await self.device_controller.commission_with_code(code)
        return data

    async def discover(self) -> List[CommissionableNode]:
        data = await self.device_controller.discover_commissionable_nodes()
        if isinstance(data, list) is False:
            return [data]
        return data

    async def close(self):
        self.logger.info("Stopping the Matter Server")
        if self.started is None:
            self.logger.info("Server not started")
            return

        await self.device_controller.stop()
        await self.storage.stop()
        self.stack.shutdown()
        self.logger.info("Cleanup complete")

    def signal_event(self, evt, data) -> None:
        self.logger.info(f"Got event {evt} with data {data}")
        pass


Registry.register_resource_creator(
    MatterController.SUBTYPE, MatterControllerServer.MODEL, ResourceCreatorRegistration(MatterControllerServer.new)
)
