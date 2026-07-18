# Browser

A real web browser tab for Biscuit — surf YouTube, Google, or any site directly inside your editor.

## Features

- Opens a browser as a proper editor tab
- Navigation toolbar (back, forward, reload)
- URL bar with Go button and Enter-key navigation
- Uses Microsoft Edge WebView2 (Chromium engine) — full JavaScript support
- Falls back to tkinterweb HtmlFrame if WebView2 runtime is unavailable

## Requirements

- **Windows** (WebView2 is Windows-only)

## Dependencies

```bash
pip install tkwebview2
```

If WebView2 runtime is not found, it will be installed automatically.

## Usage

1. Install the extension
2. Open Command Palette (`Ctrl+Shift+P`)
3. Search for "Browser: Open New Tab"
4. Type a URL and press Enter

## Development

### Project Structure

```
browser/
├── src/
│   └── browser/
│       ├── __init__.py          # Entry point
│       └── extension.py         # Main extension logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_browser.py
├── pyproject.toml
└── README.md
```

## Changelog

### 0.1.0

- Initial release
- WebView2-based browser tab
- Navigation controls (back, forward, reload)
- URL input with Enter-key navigation

## License

MIT
