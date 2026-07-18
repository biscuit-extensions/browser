from __future__ import annotations

import tkinter as tk
import typing

from biscuit.common.icons import Icons
from biscuit.common.ui import Frame, IconButton
from biscuit.editor import BaseEditor
from biscuit.extensions import Extension

if typing.TYPE_CHECKING:
    from biscuit.api import ExtensionsAPI

HAS_WEBVIEW2 = False
try:
    from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime

    if not have_runtime():
        install_runtime()
    HAS_WEBVIEW2 = True
except ImportError:
    pass

if not HAS_WEBVIEW2:
    try:
        from tkinterweb import HtmlFrame

        HAS_TKINTERWEB = True
    except ImportError:
        HAS_TKINTERWEB = False


class BrowserEditor(BaseEditor):
    name = "browser"

    def __init__(self, master, url: str = "https://www.google.com") -> None:
        super().__init__(master, path=None, editable=False)

        self.filename = "Browser"
        self._url = url
        self._browser = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_navbar()
        self._build_content()

    def _build_navbar(self) -> None:
        nav = Frame(self, bg=self.base.theme.primary_background)
        nav.grid(row=0, column=0, sticky=tk.EW)
        nav.grid_columnconfigure(3, weight=1)

        self.back_btn = IconButton(
            nav, Icons.ARROW_LEFT, event=lambda *_: self.go_back(), iconsize=14
        )
        self.back_btn.grid(row=0, column=0, padx=1, pady=2)

        self.fwd_btn = IconButton(
            nav, Icons.ARROW_RIGHT, event=lambda *_: self.go_forward(), iconsize=14
        )
        self.fwd_btn.grid(row=0, column=1, padx=1, pady=2)

        self.reload_btn = IconButton(
            nav, Icons.REFRESH, event=lambda *_: self.reload_page(), iconsize=14
        )
        self.reload_btn.grid(row=0, column=2, padx=1, pady=2)

        self.url_var = tk.StringVar(value=self._url)
        self.url_entry = tk.Entry(
            nav,
            textvariable=self.url_var,
            relief=tk.FLAT,
            font=self.base.settings.uifont,
        )
        self.url_entry.grid(row=0, column=3, sticky=tk.EW, padx=3, pady=2)
        self.url_entry.bind("<Return>", self.navigate)

        self.go_btn = IconButton(
            nav, Icons.ARROW_RIGHT, event=lambda *_: self.navigate(), iconsize=14
        )
        self.go_btn.grid(row=0, column=4, padx=2, pady=2)

    def _build_content(self) -> None:
        self.browser_container = Frame(self, bg=self.base.theme.secondary_background)
        self.browser_container.grid(row=1, column=0, sticky=tk.NSEW)
        self.browser_container.grid_columnconfigure(0, weight=1)
        self.browser_container.grid_rowconfigure(0, weight=1)

        if HAS_WEBVIEW2:
            self._init_webview2()
        elif HAS_TKINTERWEB:
            self._init_tkinterweb()
        else:
            self._init_fallback()

        self.after(100, self.navigate)

    def _init_webview2(self) -> None:
        self._browser = WebView2(self.browser_container, 100, 100)
        self._browser.grid(row=0, column=0, sticky=tk.NSEW)

    def _init_tkinterweb(self) -> None:
        self._browser = HtmlFrame(
            self.browser_container, messages_enabled=False, vertical_scrollbar=False
        )
        self._browser.grid(row=0, column=0, sticky=tk.NSEW)

    def _init_fallback(self) -> None:
        msg = (
            "Web browser requires tkwebview2 or tkinterweb.\n"
            "Install with: pip install tkwebview2"
        )
        label = tk.Label(
            self.browser_container,
            text=msg,
            bg=self.base.theme.secondary_background,
            fg=self.base.theme.secondary_foreground,
            font=("Segoe UI", 12),
            justify=tk.CENTER,
        )
        label.grid(row=0, column=0)

    def navigate(self, event: tk.Event = None) -> None:
        url = self.url_var.get().strip()
        if not url:
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            self.url_var.set(url)
        if self._browser:
            if HAS_WEBVIEW2:
                self._browser.load_url(url)
            elif HAS_TKINTERWEB:
                self._browser.load_url(url)

    def go_back(self) -> None:
        if HAS_WEBVIEW2 and self._browser and self._browser.core:
            self._browser.core.GoBack()

    def go_forward(self) -> None:
        if HAS_WEBVIEW2 and self._browser and self._browser.core:
            self._browser.core.GoForward()

    def reload_page(self) -> None:
        if self._browser:
            if HAS_WEBVIEW2:
                self._browser.reload()
            elif HAS_TKINTERWEB:
                self._browser.reload()

    def focus(self) -> None:
        self.url_entry.focus_set()

    def destroy(self) -> None:
        if HAS_WEBVIEW2 and self._browser:
            try:
                self._browser.web.Dispose()
            except Exception:
                pass
        super().destroy()


class Browser(Extension):
    def __init__(self, api: "ExtensionsAPI") -> None:
        super().__init__(api)
        self.api.logger.info("Browser extension initialised.")

    def install(self) -> None:
        self.api.commands.register_command(
            "Browser: Open New Tab", self.open_browser
        )
        self.api.notifications.info(
            "Browser extension loaded! Open via Command Palette."
        )

    def open_browser(self, *_args) -> None:
        editor = BrowserEditor(self.api.editorsmanager)
        self.api.editors.add_editor(editor)
