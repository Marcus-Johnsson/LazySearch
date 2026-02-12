import json
import os
import sys


def get_config_dir():
    """Get platform-appropriate config directory."""
    if sys.platform == 'win32':
        # Windows: use app directory
        return os.path.dirname(__file__)
    else:
        # Linux/macOS: use XDG config directory
        xdg_config = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        config_dir = os.path.join(xdg_config, 'lazysearch')
        os.makedirs(config_dir, exist_ok=True)
        return config_dir


CONFIG_FILE = os.path.join(get_config_dir(), 'config.json')

DEFAULT_CONFIG = {
    "api_key": "",
    "hotkey1": "alt+b",
    "hotkey2": "alt+g",
    "prompt_template1": "Explain briefly in 1-2 sentences: ",
    "prompt_template2": "Explain this svelte5/typescript code: "
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_api_key():
    config = load_config()
    return config.get("api_key", "")

def save_settings(settings_dict):
    config = load_config()
    config.update(settings_dict)
    save_config(config)

def get_prompt1():
    config = load_config()
    return config.get("prompt_template1", "")


def get_prompt2():
    config = load_config()
    return config.get("prompt_template2", "")
