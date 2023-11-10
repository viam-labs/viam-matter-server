# SPDX-FileCopyrightText: 2023-present HipsterBrown <headhipster@hipsterbrown.com>
#
# SPDX-License-Identifier: Apache-2.0
from viam.resource.registry import Registry, ResourceCreatorRegistration
from matter_controller_api import MatterController
from .server import MatterControllerServer

Registry.register_resource_creator(
    MatterController.SUBTYPE, MatterControllerServer.MODEL, ResourceCreatorRegistration(MatterControllerServer.new)
)
