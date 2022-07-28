# Copyright 2022 Penelope Valentine Gale
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest.mock import MagicMock

from ops.model import ActiveStatus
from ops.testing import Harness

from charm import BrassTacksCharm


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(BrassTacksCharm)
        self.harness.update_config({"delay": "0"})
        self.addCleanup(self.harness.cleanup)
        self.harness.begin_with_initial_hooks()

    def test_smoke(self):
        self.assertEqual(self.harness.model.unit.status, ActiveStatus())

    def test_on_relation_broken(self):
        relation = self.harness.charm.model.relations["brass-tack"][0]
        app = self.harness.charm.model.app
        self.harness.charm.on.brass_tack_relation_broken.emit(relation, app)

    def test_planned_action(self):
        planned = dict(num=None)
        action_event = MagicMock()
        action_event.set_results = lambda x: planned.update({'num': x['planned']})

        self.harness.charm._on_planned_action(action_event)

        self.assertEqual(planned['num'], 1)
