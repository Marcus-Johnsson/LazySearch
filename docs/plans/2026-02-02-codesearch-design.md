# LazySearch Design

Quick-lookup tool for programming terms using Gemini AI.

## Overview

A Windows system tray app that lets you select any text, press `Alt+B`, and get a brief AI-powered explanation as a toast notification.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    System Tray App                  │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Hotkey    │  │   Gemini    │  │   Config    │ │
│  │  Listener   │  │   Client    │  │   Manager   │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │        │
│         ▼                ▼                ▼        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Clipboard  │  │    Toast    │  │  Settings   │ │
│  │   Reader    │  │  Notifier   │  │   Dialog    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
```

## User Flow

1. App starts → loads config → sits in system tray
2. User selects text anywhere → presses `Alt+B`
3. App simulates Ctrl+C to capture selection
4. Sends to Gemini: "Explain briefly in 1-2 sentences: {text}"
5. Shows response as Windows toast notification

## Configuration

**Config file (`config.json`):**
```json
{
  "api_key": "your-gemini-api-key-here",
  "hotkey": "alt+b",
  "prompt_template": "Explain briefly in 1-2 sentences: {text}"
}
```

**First-run:** If no API key, prompt user with dialog.

**System tray menu:**
- Set API Key...
- Quit

## Text Capture

Simulate Ctrl+C approach:
1. Save current clipboard
2. Simulate Ctrl+C
3. Read clipboard (selected text)
4. Restore original clipboard
5. Query Gemini with captured text

## Notifications

Windows toast notifications via `winotify`:
- Duration: "long" (~25 seconds)
- Shows selected term as title
- Shows explanation as body

## Error Handling

| Error | Response |
|-------|----------|
| No API key | Dialog prompt |
| Invalid API key | Toast: "Invalid API key" |
| No internet | Toast: "Connection failed" |
| Rate limit | Toast: "Too many requests" |
| No text selected | Toast: "No text selected" |

## Dependencies

```
google-generativeai
pystray
keyboard
pyperclip
winotify
Pillow
```

## File Structure

```
LazySearch/
├── main.py           # Entry point, tray icon, hotkey setup
├── gemini_client.py  # Gemini API wrapper
├── config.py         # Config loading/saving
├── notifier.py       # Toast notifications
├── config.json       # User settings
└── requirements.txt
```

## Future Enhancements

- Custom popup window for longer responses
- Configurable hotkey via tray menu
- "More detail" follow-up queries
- Cross-platform support
