import asyncio

from viam.module.module import Module
from viam.services.service_base import ServiceBase
from .matter_controller_server import MatterControllerServer


async def main():
    """This function creates and starts a new module, after adding all the desired resources."""

    module = Module.from_args()
    module.add_model_from_registry(ServiceBase.SUBTYPE, MatterControllerServer.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
