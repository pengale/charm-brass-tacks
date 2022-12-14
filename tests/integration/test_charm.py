# Copyright 2022 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import logging
import time

from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)


async def test_smoke(ops_test: OpsTest):
    charm = await ops_test.build_charm(".")
    app = await ops_test.model.deploy(charm, num_units=2)

    await ops_test.model.block_until(lambda: app.status in ("active", "error"))

    assert app.status, "active"


async def test_delay(ops_test: OpsTest):
    app = ops_test.model.applications["brass-tacks"]
    await app.set_config({"delay": "0.1"})

    unit0 = app.units[0]
    unit1 = app.units[1]

    await unit1.destroy()
    await ops_test.model.block_until(lambda: app.status in ("maintenance", "error"))

    while app.status == "maintenance" and app.status_message:
        logger.info(app.status_message)
        time.sleep(0.05)
