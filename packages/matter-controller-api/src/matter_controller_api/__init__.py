# SPDX-FileCopyrightText: 2023-present HipsterBrown <headhipster@hipsterbrown.com>
#
# SPDX-License-Identifier: Apache-2.0
from viam.resource.registry import Registry, ResourceRegistration

from .api import MatterControllerClient, MatterControllerRPCService, MatterController, MatterNodeData

Registry.register_subtype(
    ResourceRegistration(
        MatterController, MatterControllerRPCService, lambda name, channel: MatterControllerClient(name, channel)
    )
)
