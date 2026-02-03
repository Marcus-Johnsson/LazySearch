import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

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
