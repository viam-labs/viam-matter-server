# Viam Matter Server

Created using [Hatch](https://hatch.pypa.io/latest/)

Based on [Python Matter Server](https://github.com/home-assistant-libs/python-matter-server)

-----

**Table of Contents**

- [Functionality](#functionality)
- [Installation](#installation)
- [License](#license)
- [Development](#development)

## Functionality

This project enables any [Viam](https://www.viam.com) machine to become a [Matter controller](https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/protocols/matter/overview/network_topologies.html#matter_controller) to discover, commission (a.k.a pair), and control Matter devices on the same network.

_Only Light OnOff commands are available at this time._

## Installation

This repo contains two packages:

- `matter_controller_api` (custom Viam service with generated gPRC client for Python)
- `matter_controller_server` (Viam modular resource that starts up a Matter Device Controller and uses the paired service API to communicate with the Viam SDKs)

The `matter_controller_server` can be deployed to a Viam machine as a [modular resource](https://docs.viam.com/registry/) with no configuration. (Currently available to `viam-labs` members only at the moment)

The API package (`matter_controller_api`) can be installed in a Python environment as a remote file dependency in a `requirements.txt` or `pyproject.toml` file:

```
"matter-controller-api @ git+https://github.com/viam-labs/viam-matter-server.git#egg=matter-controller-api&subdirectory=packages/matter-controller-api"
```

It can be used in with the Viam Python SDK:

```python
from matter_controller_api import MatterController
# other Viam imports

async def main():
    # create a robot client instance
    robot = await connect()

    # controller_name should match the name of the service configured in the Viam app
    controller = MatterController.from_robot(robot, name=controller_name)
    device_code = input("What is the pairing code for your device?")
    matter_node = await controller.commission(code=device_code)
    LOGGER.info(matter_node)

    LOGGER.info(f"Toggling light on Node {matter_node.node_id}")
    success = await controller.command_device(
        node_id=matter_node.node_id, endpoint_id=matter_node.endpoint_ids[0], command_name="LIGHT_TOGGLE", payload={}
    )
    LOGGER.info(f"Toggled light? {success}")

    await robot.close()
```

See `packages/matter_controller_api/client.py` for the complete sample program.


## License

`viam-matter-server` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.

## Development

[Installing Hatch](https://hatch.pypa.io/latest/install/) will make it easier to get setup but not required.

Within the `matter_controller_api` package directory, install the project dependencies within the default virtual environment:

```console
hatch run pip install .
```

With the `matter_controller_server` package directory, install the project dependencies within the dev virtual environment:

```console
hatch -e dev run pip install .
```

This depends on having the [`connectedhomeip` core Python wheels](https://github.com/home-assistant-libs/chip-wheels/blob/main/.github/workflows/build.yaml) built locally when on macos.

[DevPod](https://devpod.sh/docs/what-is-devpod) can be used to quickly scaffold a Linux dev environment in a Docker container.

```console
devpod up .
```
(when using [the CLI](https://devpod.sh/docs/developing-in-workspaces/create-a-workspace#via-devpod-cli))

**See the individual package READMEs for more information about common workflows.**
