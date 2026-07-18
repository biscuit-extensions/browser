from __future__ import annotations

import sys
from pathlib import Path

import pytest


def test_extension_imports():
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from browser.extension import Browser, BrowserEditor

    assert Browser is not None
    assert BrowserEditor is not None


def test_browser_editor_name():
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from browser.extension import BrowserEditor

    assert BrowserEditor.name == "browser"


def test_setup_exists():
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from browser import setup

    assert callable(setup)
