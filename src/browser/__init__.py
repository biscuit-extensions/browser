from __future__ import annotations

import typing

from .extension import Browser, BrowserEditor

if typing.TYPE_CHECKING:
    from biscuit.api import ExtensionsAPI


def setup(api: "ExtensionsAPI") -> None:
    api.register("browser", Browser(api))


__all__ = ["setup", "Browser", "BrowserEditor"]
