import threading
import pyperclip
from PIL import Image, ImageDraw
from pystray import Icon, MenuItem, Menu
from pynput import keyboard

import config
import notifier
import gemini_client

# Global state for hotkey detection
pressed_keys = set()
listener = None


def create_icon_image():
    img = Image.new('RGB', (100, 100), color=(0, 120, 60))
    draw = ImageDraw.Draw(img)
    draw.text((22, 12), "S", fill="white")
    return img


def get_clipboard_text():
    try:
        text = pyperclip.paste()
        if text:
            return text.strip()
    except:
        pass
    return None


def on_hotkey1():
    # Check API key
    api_key = config.get_api_key()
    if not api_key:
        notifier.show_error("No API key configured. Right-click tray icon to set.")
        return
    text = get_clipboard_text()
    if not text:
        notifier.show_error("Clipboard is empty.")
        return
    if len(text) > 500:
        text = text[:500] + "..."
    result, error = gemini_client.prompt1(text)

    if error:
        notifier.show_error(error)
    else:
        title = text[:50] + "..." if len(text) > 50 else text
        notifier.show(title, result)


def on_hotkey2():
    # Check API key
    api_key = config.get_api_key()
    if not api_key:
        notifier.show_error("No API key configured. Right-click tray icon to set.")
        return
    text = get_clipboard_text()
    if not text:
        notifier.show_error("Clipboard is empty.")
        return
    if len(text) > 500:
        text = text[:500] + "..."
    result, error = gemini_client.prompt2(text)

    if error:
        notifier.show_error(error)
    else:
        title = text[:50] + "..." if len(text) > 50 else text
        notifier.show(title, result)


def parse_hotkey(hotkey_str):
    """Parse hotkey string like 'alt+b' into modifier set and key."""
    parts = hotkey_str.lower().split('+')
    key = parts[-1]
    modifiers = set(parts[:-1])
    return modifiers, key


def check_hotkey(required_modifiers, required_key, current_key):
    """Check if the current key press matches the hotkey."""
    # Map modifier names to pynput Key objects
    modifier_map = {
        'alt': {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr},
        'ctrl': {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r},
        'shift': {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r},
        'cmd': {keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r},
    }

    # Check if all required modifiers are pressed
    for mod in required_modifiers:
        if mod in modifier_map:
            if not any(k in pressed_keys for k in modifier_map[mod]):
                return False

    # Check if the main key matches
    try:
        if hasattr(current_key, 'char') and current_key.char:
            return current_key.char.lower() == required_key
    except AttributeError:
        pass

    return False


def on_press(key):
    """Handle key press events."""
    pressed_keys.add(key)

    cfg = config.load_config()
    hotkey1 = cfg.get("hotkey1", "alt+b")
    hotkey2 = cfg.get("hotkey2", "alt+g")

    mods1, key1 = parse_hotkey(hotkey1)
    mods2, key2 = parse_hotkey(hotkey2)

    if check_hotkey(mods1, key1, key):
        threading.Thread(target=on_hotkey1, daemon=True).start()
    elif check_hotkey(mods2, key2, key):
        threading.Thread(target=on_hotkey2, daemon=True).start()


def on_release(key):
    """Handle key release events."""
    pressed_keys.discard(key)


def prompt_for_settings(icon=None):
    def show_settings_window():
        import tkinter as tk

        root = tk.Tk()
        root.title("LazySearch Settings")
        root.geometry("500x150")

        # Bring window to front and focus
        root.attributes('-topmost', True)
        root.after(100, lambda: root.attributes('-topmost', False))
        root.focus_force()

        cfg = config.load_config()

        # API Key
        tk.Label(root, text="API Key:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        api_entry = tk.Entry(root, width=50)
        api_entry.insert(0, cfg.get("api_key", ""))
        api_entry.grid(row=0, column=1, padx=10, pady=5)

        # Prompt 1
        tk.Label(root, text="Prompt 1:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        prompt1_entry = tk.Entry(root, width=50)
        prompt1_entry.insert(0, cfg.get("prompt_template1", ""))
        prompt1_entry.grid(row=1, column=1, padx=10, pady=15)

        # Prompt 2
        tk.Label(root, text="Prompt 2:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        prompt2_entry = tk.Entry(root, width=50)
        prompt2_entry.insert(0, cfg.get("prompt_template2", ""))
        prompt2_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_settings():
            settings = {
                "api_key": api_entry.get().strip(),
                "prompt_template1": prompt1_entry.get().strip(),
                "prompt_template2": prompt2_entry.get().strip()
            }
            config.save_settings(settings)
            notifier.show("LazySearch", "Settings saved.")
            root.destroy()

        def cancel():
            root.destroy()

        # Handle X button close
        root.protocol("WM_DELETE_WINDOW", cancel)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Save", command=save_settings, width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", command=cancel, width=10).pack(side="left", padx=5)

        root.mainloop()

    # Run tkinter in a separate thread to avoid blocking pystray
    settings_thread = threading.Thread(target=show_settings_window, daemon=True)
    settings_thread.start()


def quit_app(icon):
    """Clean shutdown."""
    global listener
    if listener:
        listener.stop()
    icon.stop()


def setup_tray():
    menu = Menu(
        MenuItem("LazySearch", lambda: None, enabled=False),
        Menu.SEPARATOR,
        MenuItem("Settings", prompt_for_settings),
        Menu.SEPARATOR,
        MenuItem("Quit", quit_app)
    )

    icon = Icon(
        name="LazySearch",
        icon=create_icon_image(),
        title="LazySearch",
        menu=menu
    )

    return icon


def prompt_for_settings_blocking():
    """Show settings window and wait for it to close (for startup use)."""
    import tkinter as tk

    root = tk.Tk()
    root.title("LazySearch Settings")
    root.geometry("500x150")

    cfg = config.load_config()

    # API Key
    tk.Label(root, text="API Key:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    api_entry = tk.Entry(root, width=50)
    api_entry.insert(0, cfg.get("api_key", ""))
    api_entry.grid(row=0, column=1, padx=10, pady=5)

    # Prompt 1
    tk.Label(root, text="Prompt 1:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    prompt1_entry = tk.Entry(root, width=50)
    prompt1_entry.insert(0, cfg.get("prompt_template1", ""))
    prompt1_entry.grid(row=1, column=1, padx=10, pady=15)

    # Prompt 2
    tk.Label(root, text="Prompt 2:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    prompt2_entry = tk.Entry(root, width=50)
    prompt2_entry.insert(0, cfg.get("prompt_template2", ""))
    prompt2_entry.grid(row=2, column=1, padx=10, pady=5)

    def save_settings():
        settings = {
            "api_key": api_entry.get().strip(),
            "prompt_template1": prompt1_entry.get().strip(),
            "prompt_template2": prompt2_entry.get().strip()
        }
        config.save_settings(settings)
        notifier.show("LazySearch", "Settings saved.")
        root.destroy()

    def cancel():
        root.destroy()

    # Handle X button close
    root.protocol("WM_DELETE_WINDOW", cancel)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(button_frame, text="Save", command=save_settings, width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", command=cancel, width=10).pack(side="left", padx=5)

    root.mainloop()


def main():
    global listener

    if not config.get_api_key():
        prompt_for_settings_blocking()

    # Start global hotkey listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    icon = setup_tray()
    icon.run()


if __name__ == "__main__":
    main()
