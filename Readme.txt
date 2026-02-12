  ---
  LazySearch

  LazySearch is a lightweight system tray utility that provides instant AI-powered explanations for any text on your clipboard using Google's Gemini API. Works on Windows and Linux.

  How It Works

  1. Copy any text to your clipboard
  2. Press a hotkey (default: Alt+B or Alt+G)
  3. Receive an AI-generated explanation as a desktop notification

  Next step:
  1. Add in settings to change keybinds

  Features

  - Cross-Platform - Works on Windows and Linux
  - System Tray Integration - Runs quietly in the background with minimal footprint
  - Two Customizable Prompts - Configure different prompt templates for different use cases:
    - Prompt 1 (Alt+B): General brief explanations
    - Prompt 2 (Alt+G): Code explanations (default: Svelte5/TypeScript)
  - Hotkey Activated - No need to switch windows or open a browser
  - Desktop Notifications - Results appear as native desktop notifications
  - Configurable Settings - Right-click the tray icon to set your API key and customize prompts

  Requirements

  - Python 3.x
  - Google Gemini API key

  Installation

  Windows:
    pip install -r requirements.txt

  Linux (Ubuntu/Debian):
    sudo apt install xclip python3-tk libgirepository1.0-dev gir1.2-appindicator3-0.1
    pip install -r requirements.txt

  Linux (Fedora):
    sudo dnf install xclip python3-tkinter libappindicator-gtk3
    pip install -r requirements.txt                                                                                                                                                                                                          
                                                                                                                                                                                                                                           
  Usage                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                           
  python main.py                                                                                                                                                                                                                           
                                                                                                                                                                                                                                           
  On first run, you'll be prompted to enter your Gemini API key. After that, the app runs in the system tray - copy text and use the hotkeys to get instant explanations.                                                                  
                                                                                                                                                                                                                                           
  Dependencies                                                                                                                                                                                                                             
                                                                                                                                                                                                                                           
  - google-generativeai - Gemini API client                                                                                                                                                                                                
  - pystray - System tray functionality                                                                                                                                                                                                    
  - pynput - Global hotkey detection                                                                                                                                                                                                       
  - pyperclip - Clipboard access                                                                                                                                                                                                           
  - plyer - Desktop notifications                                                                                                                                                                                                          
  - Pillow - Tray icon generation                                                                                                                                                                                                          
                                                                                                                                                                                                                                           
  ---   