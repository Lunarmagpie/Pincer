# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import List, Tuple

from ..core.dispatch import GatewayDispatch


async def payload_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[GatewayDispatch]]:
    """Invoked when basically anything is received from gateway.

    Parameters
    ----------
    payload : :class:¬pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.core.dispatch.GatewayDispatch`]]
        ``on_payload`` and a ``payload``
    """
    return "on_payload", [payload]


def export():
    """Export the middleware"""
    return payload_middleware
