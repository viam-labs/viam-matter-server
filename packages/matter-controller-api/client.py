import asyncio
import os

from src.matter_controller_api import MatterController

from viam.logging import getLogger, logging
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

robot_secret = os.getenv('ROBOT_SECRET') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''
controller_name = os.getenv('MATTER_CONTROLLER_NAME') or 'matter-controller'

LOGGER = getLogger(__name__)


async def connect():
    creds = Credentials(type="robot-location-secret", payload=robot_secret)
    opts = RobotClient.Options(refresh_interval=0, dial_options=DialOptions(credentials=creds), log_level=logging.DEBUG)
    return await RobotClient.at_address(robot_address, opts)


async def main():
    robot = await connect()

    controller = MatterController.from_robot(robot, name=controller_name)
    device_code = input("What is the pairing code for your device? ")
    matter_node = await controller.commission(code=device_code)
    LOGGER.info(matter_node)

    LOGGER.info(f"Toggling light on Node {matter_node.node_id}")
    for endpoint in matter_node.endpoint_ids:
        try:
            success = await controller.command_device(
                node_id=matter_node.node_id, endpoint_id=endpoint, command_name="LIGHT_TOGGLE", payload={}
            )
            LOGGER.info(f"Toggled light? {success}")
        except:
            LOGGER.error(f"Unable to toggle on endpoint {endpoint}")

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
