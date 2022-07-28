"""Planned Units Plus

This library provides some enhancements for the planned units functionality.
"""

import typing

# The unique Charmhub library identifier, never change it
LIBID = "ffd4b147a8a84ba8a9571ebedf11df0b"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1


def projected_net(charm):
    """Returns a count of current and planned units, minus units that are in a 'dying' state.

    """
    app_state = charm.model._backend._run('goal-state', return_output=True, use_json=True)
    app_state = typing.cast(typing.Dict[str, typing.List[str]], app_state)
    units = [unit for unit in app_state.get('units', []) if unit['life'] != 'dying']
    
    return len(units)
    


