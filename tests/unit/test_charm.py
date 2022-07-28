# Copyright 2022 Penelope Valentine Gale
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest

from ops.model import ActiveStatus
from ops.testing import Harness

from charm import BrassTacksCharm


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(BrassTacksCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin_with_initial_hooks()

    def test_smoke(self):
        self.assertEqual(self.harness.model.unit.status, ActiveStatus())

    def test_on_relation_broken(self):
        relation = self.harness.charm.model.relations["brass-tack"][0]
        app = self.harness.charm.model.app
        self.harness.charm.on.brass_tack_relation_broken.emit(relation, app)
