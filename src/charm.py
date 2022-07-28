#!/usr/bin/env python3
# Copyright 2022 Penelope Valentine Gale
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Brass tacks."""

import logging
import time

from charms.brass_tacks.v0.planned_units_plus import projected_net
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus

logger = logging.getLogger(__name__)


class BrassTacksCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on["brass-tack"].relation_broken, self._on_broken)
        self.framework.observe(self.on.planned_action, self._on_planned_action)

    def _on_install(self, event):
        self.unit.status = ActiveStatus()

    def _on_planned_action(self, event):
        self.model._backend._run = lambda *args, **kwargs: {
            'units': [
                {'life': 'running'},  # TODO lookup real value
                {'life': 'dying'}
                ]
        }
        event.set_results({"planned": projected_net(self)})

    def _on_broken(self, event):
        delay = float(self.config["delay"])
        logger.info("Processing broken relation with delay {}s.".format(delay))
        logger.info("Planned unit count: {}".format(self.model.app.planned_units()))
        monologue = """
Go get thee hence, for I will not away.
What’s here? A cup clos’d in my true love’s hand?
Poison, I see, hath been his timeless end.
O churl, drunk all, and left no friendly drop
To help me after? I will kiss thy lips
Haply some poison yet doth hang on them
To make me die with a restorative.
Thy lips are warm.
...
Yea, noise? Then I’ll be brief. O happy dagger
This is thy sheath; there rust, and let me die.
"""

        for line in monologue.split("\n"):
            self.unit.status = MaintenanceStatus(line)
            time.sleep(delay)


if __name__ == "__main__":
    main(BrassTacksCharm)
